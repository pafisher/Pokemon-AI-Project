import weather
import status
import log

SELF = "SELF"
FOE = "FOE"

STATUS = "STATUS"
PHYSICAL = "PHYSICAL"
SPECIAL = "SPECIAL"

def NOP(arg1 = None, arg2 = None, arg3 = None):
	return None

class BattleMoveTemplate:
	def __init__(self, **kwargs):
		self.num = kwargs.get("num", 0)
		self.accuracy = kwargs.get("accuracy", 0)
		self.base_power = kwargs.get("base_power", 0)
		self.category = kwargs.get("category", "UNDEFINED")
		self.is_viable = kwargs.get("is_viable", True)
		self.name = kwargs.get("name", "UNDEFINED")
		self.pp = kwargs.get("pp", 0)
		self.priority = kwargs.get("priority", 0)
		self.flags = kwargs.get("flags", [])
		self.volatile_status = kwargs.get("volatile_status", "UNDEFINED")
		self.critRatio = kwargs.get("critRatio", 0)
		self.drain = kwargs.get("drain", 0)
		self.sleepUsable = kwargs.get("sleepUsable", False)
		self.onStart = kwargs.get("onStart", NOP)
		self.onMoveAccuracy = kwargs.get("onMoveAccuracy", NOP)
		self.onTryHit = kwargs.get("onTryHit", NOP)
		self.onTry = kwargs.get("onTry", NOP)
		self.onBasePower = kwargs.get("onBasePower", NOP)
		self.onHit = kwargs.get("onHit", NOP)
		self.boosts = kwargs.get("boosts", [])
		self.secondary = kwargs.get("secondary", [])
		self.target = kwargs.get("target", "UNDEFINED")
		self.element = kwargs.get("element", "TYPELESS")

class Modifier:
	def __init__(self, chance, stat, target, amount = 0):
		self.chance = chance
		self.stat = stat # stat identifier string, or if it's a status move, status identifier string
		self.target = target
		self.amount = amount # number of levels stat increases/decreases, or if it's a status move, number of turns to be afflicted (e.g. rest=>3)

def BLIZZARDonMoveAccuracy():
	if (weather.get_weather() == weather.HAIL):
		return -1
	else:
		return 1

def RAINDANCEonStart(target):
	weather.set_weather(weather.RAINDANCE, 5)

def RESTonHit(target):
	if (target.hp >= target.max_hp or not target.set_status(status.SLP, True)):
		log.message("But the move failed")
		# return (False, "FAILED")
		return False
	target.heal(target.max_hp)
	target.status_counter = 3

def SNOREonTryHit(source):
	if (source.status != status.SLP):
		log.message("But the move failed")
		# return (False, " is not asleep")
		return False
	# return (True,)
	return True

def SOLARBEAMonTry(attacker, defender, move):
	if (attacker.remove_volatile(status.TWOTURNMOVE)):
		# return (True,)
		return True
	if (weather.get_weather() in [weather.SUNNYDAY, weather.DESOLATELAND]):
		# return (True,)
		return True
	attacker.add_volatile(status.TWOTURNMOVE, "SOLARBEAM")
	log.message(attacker.template.species + " is gathering light")
	# return (False, " is gathering sunlight")
	return False
def SOLARBEAMonBasePower(base_power, pokemon, target):
	if (weather.get_weather() in [weather.RAINDANCE, weather.PRIMORDIALSEA, weather.SANDSTORM, weather.HAIL]):
		return base_power * 0.5

def SUNNYDAYonStart(target):
	weather.set_weather(weather.SUNNYDAY, 5)

def SYNTHESISonHit(pokemon):
	if (weather.get_weather() in [weather.SUNNYDAY, weather.DESOLATELAND]):
		pokemon.heal(pokemon.max_hp * 0.667)
	elif (weather.get_weather() in [weather.RAINDANCE, weather.PRIMORDIALSEA, weather.SANDSTORM, weather.HAIL]):
		pokemon.heal(pokemon.max_hp * 0.25)
	else:
		pokemon.heal(pokemon.max_hp * 0.5)

def THUNDERonMoveAccuracy():
	if (weather.get_weather() in [weather.RAINDANCE, weather.PRIMORDIALSEA]):
		return -1
	elif (weather.get_weather() in [weather.SUNNYDAY, weather.DESOLATELAND]):
		return 5.0/7.0

battle_move = {
	"AMNESIA" : BattleMoveTemplate(
		num = 133,
		accuracy = -1,
		base_power = 0,
		category = "STATUS",
		name = "Amnesia",
		pp = 20,
		priority = 0,
		flags = ["SNATCH"],
		boosts = [Modifier(100, "SPD", SELF, 2)],
		target = SELF,
		element = "PSYCHIC"),
	"BLIZZARD" : BattleMoveTemplate(
		num = 59,
		accuracy = 70,
		base_power = 110,
		category = "SPECIAL",
		is_viable = True, # don't know if this is necessary
		name = "Blizzard",
		pp = 5,
		priority = 0,
		flags = ["PROTECT", "MIRROR"],
		onMoveAccuracy = BLIZZARDonMoveAccuracy,
		secondary = [Modifier(10, "FRZ", FOE)],
		target = FOE,
		element = "ICE"),
	"BODYSLAM" : BattleMoveTemplate(
		num = 34,
		accuracy = 100,
		base_power = 85,
		category = "PHYSICAL",
		is_viable = True, # don't know if this is necessary
		name = "Body Slam",
		pp = 15,
		priority = 0,
		flags = ["CONTACT", "PROTECT", "MIRROR", "NONSKY"],
		secondary = [Modifier(30, "PAR", FOE)],
		target = FOE,
		element = "NORMAL"),
	"CHARM" : BattleMoveTemplate(
		num = 204,
		accuracy = 100,
		base_power = 0,
		category = "STATUS",
		name = "Charm",
		pp = 20,
		priority = 0,
		flags = ["PROTECT", "REFLECTABLE", "MIRROR"],
		boosts = [Modifier(100, "ATK", FOE, -2)],
		target = FOE,
		element = "NORMAL"),
	"FIRESPIN" : BattleMoveTemplate(
		num = 83,
		accuracy = 85,
		base_power = 35,
		category = "SPECIAL",
		name = "Fire Spin",
		pp = 15,
		priority = 0,
		flags = ["PROTECT", "MIRROR"],
		volatile_status = "PARTIALLYTRAPPED",
		target = FOE,
		element = "FIRE"),
	"FLAMETHROWER" : BattleMoveTemplate(
		num = 53,
		accuracy = 100,
		base_power = 90,
		category = "SPECIAL",
		is_viable = True, # don't know if this is necessary
		name = "Flamethrower",
		pp = 15,
		priority = 0,
		flags = ["PROTECT", "MIRROR"],
		secondary = [Modifier(10, "BRN", FOE)],
		target = FOE,
		element = "FIRE"),
	"GIGADRAIN" : BattleMoveTemplate(
		num = 202,
		accuracy = 100,
		base_power = 75,
		category = "SPECIAL",
		is_viable = True, # don't know if this is necessary
		name = "Giga Drain",
		pp = 10,
		priority = 0,
		flags = ["PROTECT", "MIRROR", "HEAL"],
		drain = 0.5,
		target = FOE,
		element = "GRASS"),
	"MUDSLAP" : BattleMoveTemplate(
		num = 189,
		accuracy = 100,
		base_power = 20,
		category = "SPECIAL",
		name = "Mud-Slap",
		pp = 10,
		priority = 0,
		flags = ["PROTECT", "MIRROR"],
		boosts = [Modifier(100, "ACC", FOE, -1)],
		target = FOE,
		element = "GROUND"),
	"PSYCHIC" : BattleMoveTemplate(
		num = 94,
		accuracy = 100,
		base_power = 90,
		category = "SPECIAL",
		is_viable = True, # don't know if this is necessary
		name = "Psychic",
		pp = 10,
		priority = 0,
		flags = ["PROTECT", "MIRROR"],
		boosts = [Modifier(10, "SPD", FOE, -1)],
		target = FOE,
		element = "PSYCHIC"),
	"QUICKATTACK" : BattleMoveTemplate(
		num = 98,
		accuracy = 100,
		base_power = 40,
		category = "PHYSICAL",
		name = "Quick Attack",
		pp = 30,
		priority = 1,
		flags = ["CONTACT", "PROTECT", "MIRROR"],
		target = FOE,
		element = "NORMAL"),
	"RAINDANCE" : BattleMoveTemplate(
		num = 240,
		accuracy = -1,
		base_power = 0,
		category = "STATUS",
		name = "Rain Dance",
		pp = 5,
		priority = 0,
		flags = [],
		onStart = RAINDANCEonStart,
		target = SELF,
		element = "WATER"),
	"REFLECT" : BattleMoveTemplate(
		num = 115,
		accuracy = -1,
		base_power = 0,
		category = "STATUS",
		is_viable = True, # don't know if this is necessary
		name = "Reflect",
		pp = 20,
		priority = 0,
		flags = ["SNATCH"],
		secondary = [Modifier(100, "REFLECT", SELF)],
		target = SELF,
		element = "PSYCHIC"),
	"REST" : BattleMoveTemplate(
		num = 156,
		accuracy = -1,
		base_power = 0,
		category = "STATUS",
		is_viable = True, # don't know if this is necessary
		name = "Rest",
		pp = 10,
		priority = 0,
		flags = ["SNATCH", "HEAL"],
		onHit = RESTonHit,
		target = SELF,
		element = "PSYCHIC"),
	"SLASH" : BattleMoveTemplate(
		num = 163,
		accuracy = 100,
		base_power = 70,
		category = "PHYSICAL",
		name = "Slash",
		pp = 20,
		priority = 0,
		flags = ["CONTACT", "PROTECT", "MIRROR"],
		critRatio = 2,
		target = FOE,
		element = "NORMAL"),
	"SNORE" : BattleMoveTemplate(
		num = 173,
		accuracy = 100,
		base_power = 50,
		category = "SPECIAL",
		name = "Snore",
		pp = 15,
		priority = 0,
		flags = ["PROTECT", "MIRROR", "SOUND", "AUTHENTIC"],
		sleepUsable = True,
		onTryHit = SNOREonTryHit,
		secondary = [Modifier(30, "FLINCH", FOE)],
		target = FOE,
		element = "NORMAL"),
	"SOLARBEAM" : BattleMoveTemplate(
		num = 76,
		accuracy = 100,
		base_power = 120,
		category = "SPECIAL",
		name = "Solar Beam",
		pp = 10,
		priority = 0,
		flags = ["CHARGE", "PROTECT", "MIRROR"],
		onTry = SOLARBEAMonTry,
		onBasePowerPriority = 4,
		onBasePower = SOLARBEAMonBasePower,
		target = FOE,
		element = "GRASS"),
	"SUNNYDAY" : BattleMoveTemplate(
		num = 241,
		accuracy = -1,
		base_power = 0,
		category = "STATUS",
		name = "Sunny Day",
		pp = 5,
		priority = 0,
		flags = [],
		onStart = SUNNYDAYonStart,
		target = SELF,
		element = "FIRE"),
	"SURF" : BattleMoveTemplate(
		num = 57,
		accuracy = 100,
		base_power = 90,
		category = "SPECIAL",
		is_viable = True, # don't know if this is necessary
		name = "Surf",
		pp = 15,
		priority = 0,
		flags = ["PROTECT", "MIRROR", "NONSKY"],
		target = FOE,
		element = "WATER"),
	"SWIFT" : BattleMoveTemplate(
		num = 129,
		accuracy = -1,
		base_power = 60,
		category = "SPECIAL",
		name = "Swift",
		pp = 20,
		priority = 0,
		flags = ["PROTECT", "MIRROR"],
		target = FOE,
		element = "NORMAL"),
	"SYNTHESIS" : BattleMoveTemplate(
		num = 235,
		accuracy = -1,
		base_power = 0,
		category = "STATUS",
		is_viable = True, # don't know if this is necessary
		name = "Synthesis",
		pp = 5,
		priority = 0,
		flags = ["SNATCT", "HEAL"],
		onHit = SYNTHESISonHit,
		target = SELF,
		element = "GRASS"),
	"THUNDER" : BattleMoveTemplate(
		num = 87,
		accuracy = 70,
		base_power = 110,
		category = "SPECIAL",
		is_viable = True, # don't know if this is necessary
		name = "Thunder",
		pp = 10,
		priority = 0,
		flags = ["PROTECT", "MIRROR"],
		onMoveAccuracy = THUNDERonMoveAccuracy,
		secondary = [Modifier(30, "PAR", FOE)],
		target = FOE,
		element = "ELECTRIC"),
	"THUNDERBOLT" : BattleMoveTemplate(
		num = 85,
		accuracy = 100,
		base_power = 90,
		category = "SPECIAL",
		is_viable = True, # don't know if this is necessary
		name = "Thunderbolt",
		pp = 15,
		priority = 0,
		flags = ["PROTECT", "MIRROR"],
		secondary = [Modifier(10, "PAR", FOE)],
		target = FOE,
		element = "ELECTRIC"),
	"WHIRLPOOL" : BattleMoveTemplate(
		num = 250,
		accuracy = 85,
		base_power = 35,
		category = "SPECIAL",
		name = "Whirlpool",
		pp = 15,
		priority = 0,
		flags = ["PROTECT", "MIRROR"],
		volatileStatus = 'PARTIALLYTRAPPED',
		target = FOE,
		element = "WATER"),
	"WINGATTACK" : BattleMoveTemplate(
		num = 17,
		accuracy = 100,
		base_power = 60,
		category = "PHYSICAL",
		name = "Wing Attack",
		pp = 35,
		priority = 0,
		flags = ["CONTACT", "PROTECT", "MIRROR", "DISTANCE"],
		target = FOE,
		element = "FLYING"),
}