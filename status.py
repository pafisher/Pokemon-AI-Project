import fakerandom
import weather
import log

# statuses
BRN = "BRN"
PAR = "PAR"
SLP = "SLP"
FRZ = "FRZ"
PSN = "PSN"
TOX = "TOX"

# volatile statuses
CONFUSION = "CONFUSION"
FLINCH = "FLINCH"
PARTIALLYTRAPPED = "PARTIALLYTRAPPED"
REFLECT = "REFLECT"
TWOTURNMOVE = "TWOTURNMOVE"

def NOP(arg1 = None, arg2 = None, arg3 = None):
	return None

class BattleStatus:
	def __init__(self, name, effectType, **kwargs):
		self.name = name
		self.effectType = effectType
		self.noCopy = kwargs.get("noCopy", False)
		self.onStart = kwargs.get("onStart", NOP)
		self.onResidualOrder = kwargs.get("onResidualOrder", 0) # not sure if it should be low or high for default
		self.onResidual = kwargs.get("onResidual", NOP)
		self.onModifySpe = kwargs.get("onModifySpe", NOP)
		self.onBeforeMovePriority = kwargs.get("onBeforeMovePriority", 0) # not sure if it should be low or high for default
		self.onBeforeMove = kwargs.get("onBeforeMove", NOP)
		self.onModifyMove = kwargs.get("onModifyMove", NOP)
		self.onTrySwitchAction = kwargs.get("onTrySwitchAction", NOP)
		self.onHit = kwargs.get("onHit", NOP)
		self.onSwitchIn = kwargs.get("onSwitchIn", NOP)

def BRNonStart(target):#, source, sourceEffect):
	# if (sourceEffect and source == "FLAME ORB" and target.set_status(BRN)):
	if (target.set_status(BRN)):
		log.message(target.template.species + " was burned")
		# target.set_status_source("FLAME ORB")
def BRNonResidual(pokemon):
	log.message(pokemon.template.species + " was hurt by its burn")
	pokemon.damage(pokemon.max_hp / 8)

def PARonStart(target):
	if (target.set_status(PAR)):
		log.message(target.template.species + " was paralyzed")
def PARonModifySpe(speMod, pokemon):
	if (not pokemon.ability == "QUICKFEET"):
		return speMod * 0.25
def PARonBeforeMove(pokemon, target = None, move = None):
	if (fakerandom.fakerandom() < 0.25):
		log.message(pokemon.template.species + " was paralyzed and couldn't move")
		# return (False, PAR)
		return False
	# return (True,)
	return True

def SLPonStart(target):
	if (target.set_status(SLP)):
		log.message(target.template.species + " fell asleep")
		target.set_status_counter(fakerandom.fakerandint(1, 3))
def SLPonBeforeMove(pokemon, target, move):
	if (pokemon.ability == "EARLYBIRD"):
		pokemon.decrement_status_counter()
	pokemon.decrement_status_counter()
	if (pokemon.get_status_counter <= 0):
		pokemon.cure_status()
		log.message(pokemon.template.species + " woke up")
		# return (True,)
		return True
	if (move.sleepUsable):
		# return (True,)
		return True
	log.message(pokemon.template.species + " is fast asleep")
	# return (False, SLP)
	return False

def FRZonStart(target):
	if (target.set_status(FRZ)):
		log.message(target.template.species + " was frozen solid")
def FRZonBeforeMove(pokemon, target, move):
	if (move.flags["DEFROST"]):
		log.message(pokemon.template.species + " thawed out")
		pokemon.cure_status()
		# return (True, )
		return True
	if (fakerandom.fakerandom() < 0.2):
		log.message(pokemon.template.species + " thawed out")
		pokemon.cure_status()
		# return (True,)
		return True
	log.message(pokemon.template.species + " is frozen solid")
	# return (False, FRZ)
	return False
# def FRZonModifyMove(move, pokemon): # don't think we need this
# 	if (move.flags["DEFROST"]):
# 		pokemon.cure_status()
def FRZonHit(target, source, move):
	if (move.thaws_target or move.element == "FIRE" and move.category != "STATUS"):
		log.message(target.template.species + " thawed out")
		target.cure_status()

def PSNonStart(target):
	if (target.set_status(PSN)):
		log.message(target.template.species + " was poisoned")
def PSNonResidual(pokemon):
	log.message(pokemon.template.species + " was hurt by poison")
	pokemon.damage(pokemon.max_hp / 8)

def TOXonStart(target, source, sourceEffect):
	# if (sourceEffect and source == "TOXIC ORB" and target.set_status(TOX)):
	if (target.set_status(TOX)):
		log.message(target.template.species + " was badly poisoned")
		# target.set_status_source("TOXIC ORB")
		target.set_status_counter(0)
def TOXonSwitchIn():
	target.set_status_counter(0)
def TOXonResidual(pokemon):
	if (pokemon.get_status_counter < 15):
		pokemon.increment_status_counter()
	log.message(pokemon.template.species + " was hurt by poison")
	pokemon.damage((pokemon.max_hp / 16) * pokemon.get_status_counter())

def CONFUSIONonStart(target, source, sourceEffect):
	# if (sourceEffect and source == "LOCKEDMOVE" and target.add_volatile(CONFUSION)):
	if (target.add_volatile(CONFUSION)):
		log.message(target.template.species + " became confused")
		# target.confusion_source = "FATIGUE"
		target.confusion_count = fakerandom.fakerandint(2, 6)
# def CONFUSIONonEnd(target):
# 	target.add_volatile(CONFUSION)
def CONFUSIONonBeforeMove(pokemon, target = None, move = None):
	pokemon.confusion_count -= 1
	if (pokemon.confusion_count <= 0 and pokemon.remove_volatile(CONFUSION)):
		log.message(pokemon.template.species + " snapped out of confusion")
		# return (True,)
		return True
	if (fakerandom.fakerandom() < 0.5):
		# return (True,)
		return True
	log.message(pokemon.template.species + " hurt itself in confusion")
	pokemon.damage(battle.get_damage(pokemon, pokemon, moves.hitself)) # need to make sure there's a typless move for confusion to simulate hitting itself
	# return (False, CONFUSION)
	return False

# def FLINCHonStart(target): # may need to add - not in javascript version
# 	target.add_volatile("FLINCH")
def FLINCHonBeforeMove(pokemon, target = None, move = None):
	# target.remove_volatile("FLINCH")
	log.message(pokemon.template.species + " flinched")
	# return (False, FLINCH)
	return False
def FLINCHonEnd(pokemon): # may need to add - not in javascript version
	target.remove_volatile("FLINCH")

# trapped: {
# 		noCopy: true,
# 		onTrySwitchAction: function (pokemon) {
# 			pokemon.tryTrap();
# 		},
# 		onStart: function (target) {
# 			this.add('-activate', target, 'trapped');
# 		}
# 	},
# 	trapper: {
# 		noCopy: true
# 	},

def PARTIALLYTRAPPEDonStart(pokemon, source):
	if (source.item == "GRIPCLAW"):
		pokemon.partiallytrapped_count = 8
	else:
		pokemon.partiallytrapped_count = fakerandom.fakerandint(5, 7)
	if (pokemon.add_volatile(PARTIALLYTRAPPED)):
		log.message(pokemon.template.species + " was trapped")
		pokemon.partiallytrapped_source = source
def PARTIALLYTRAPPEDonResidual(pokemon):
	if (not pokemon.partiallytrapped_source.isActive or pokemon.partiallytrapped_source.currenthp <= 0):
		log.message(pokemon.template.species + " escaped from the trap")
		pokemon.remove_volatile(PARTIALLYTRAPPED)
		return
	log.message(pokemon.template.species + " was hurt by the trap")
	if (pokemon.partiallytrapped_source.item == "BINDINGBAND"):
		pokemon.damage(pokemon.max_hp / 6)
	else:
		pokemon.damage(pokemon.max_hp / 8)
# def PARTIALLYTRAPPEDonEnd(pokemon):
# 	pokemon.add_volatile(PARTIALLYTRAPPED)
def PARTIALLYTRAPPEDonTrySwitchAction(pokemon):
	if (pokemon.try_trap()):
		log.message(pokemon.template.species + " is trapped and can't switch out")
		return True
	return False

	# lockedmove: {
	# 	// Outrage, Thrash, Petal Dance...
	# 	duration: 2,
	# 	onResidual: function (target) {
	# 		if (target.status === 'slp') {
	# 			// don't lock, and bypass confusion for calming
	# 			delete target.volatiles['lockedmove'];
	# 		}
	# 		this.effectData.trueDuration--;
	# 	},
	# 	onStart: function (target, source, effect) {
	# 		this.effectData.trueDuration = this.random(2, 4);
	# 		this.effectData.move = effect.id;
	# 	},
	# 	onRestart: function () {
	# 		if (this.effectData.trueDuration >= 2) {
	# 			this.effectData.duration = 2;
	# 		}
	# 	},
	# 	onEnd: function (target) {
	# 		if (this.effectData.trueDuration > 1) return;
	# 		target.addVolatile('confusion');
	# 	},
	# 	onLockMove: function (pokemon) {
	# 		return this.effectData.move;
	# 	}
	# },
def TWOTURNMOVEonStart(target, source):
	print "TWOTURNMOVE START TEST"
	target.add_volatile(status.TWOTURNMOVE, source)
def TWOTURNMOVEonEnd(target):
	print "TWOTURNMOVE START TEST"
	target.removeVolatile(status.TWOTURNMOVE)
# not sure if we need these next two
# def TWOTURNMOVEonLockMove():
# 	return this.effectData.move
# def TWOTURNMOVEonLockMoveTarget():
# 	return this.effectData.targetLoc
	# choicelock: {
	# 	onStart: function (pokemon) {
	# 		if (!this.activeMove.id || this.activeMove.sourceEffect && this.activeMove.sourceEffect !== this.activeMove.id) return false;
	# 		this.effectData.move = this.activeMove.id;
	# 	},
	# 	onDisableMove: function (pokemon) {
	# 		if (!pokemon.getItem().isChoice || !pokemon.hasMove(this.effectData.move)) {
	# 			pokemon.removeVolatile('choicelock');
	# 			return;
	# 		}
	# 		if (pokemon.ignoringItem()) {
	# 			return;
	# 		}
	# 		var moves = pokemon.moveset;
	# 		for (var i = 0; i < moves.length; i++) {
	# 			if (moves[i].id !== this.effectData.move) {
	# 				pokemon.disableMove(moves[i].id, false, this.effectData.sourceEffect);
	# 			}
	# 		}
	# 	}
	# },
	# mustrecharge: {
	# 	duration: 2,
	# 	onBeforeMovePriority: 11,
	# 	onBeforeMove: function (pokemon) {
	# 		this.add('cant', pokemon, 'recharge');
	# 		pokemon.removeVolatile('mustrecharge');
	# 		return false;
	# 	},
	# 	onLockMove: function (pokemon) {
	# 		this.add('-mustrecharge', pokemon);
	# 		return 'recharge';
	# 	}
	# },
	# futuremove: {
	# 	// this is a side condition
	# 	onStart: function (side) {
	# 		this.effectData.positions = [];
	# 		for (var i = 0; i < side.active.length; i++) {
	# 			this.effectData.positions[i] = null;
	# 		}
	# 	},
	# 	onResidualOrder: 3,
	# 	onResidual: function (side) {
	# 		var finished = true;
	# 		for (var i = 0; i < side.active.length; i++) {
	# 			var posData = this.effectData.positions[i];
	# 			if (!posData) continue;

	# 			posData.duration--;

	# 			if (posData.duration > 0) {
	# 				finished = false;
	# 				continue;
	# 			}

	# 			// time's up; time to hit! :D
	# 			var target = side.foe.active[posData.targetPosition];
	# 			var move = this.getMove(posData.move);
	# 			if (target.fainted) {
	# 				this.add('-hint', '' + move.name + ' did not hit because the target is fainted.');
	# 				this.effectData.positions[i] = null;
	# 				continue;
	# 			}

	# 			this.add('-end', target, 'move: ' + move.name);
	# 			target.removeVolatile('Protect');
	# 			target.removeVolatile('Endure');

	# 			if (posData.moveData.ignoreImmunity === undefined) {
	# 				posData.moveData.ignoreImmunity = false;
	# 			}

	# 			if (target.hasAbility('wonderguard') && this.gen > 5) {
	# 				this.debug('Wonder Guard immunity: ' + move.id);
	# 				if (target.runEffectiveness(move) <= 0) {
	# 					this.add('-activate', target, 'ability: Wonder Guard');
	# 					this.effectData.positions[i] = null;
	# 					return null;
	# 				}
	# 			}

	# 			// Prior to gen 5, these moves had no STAB and no effectiveness.
	# 			// This is done here and to moveData's element for two reasons:
	# 			// - modifyMove event happens before the moveHit function is run.
	# 			// - moveData here is different from move, as one is generated here and the other by the move itself.
	# 			// So here we centralise any future hit move getting elementless on hit as it should be.
	# 			if (this.gen < 5) {
	# 				posData.moveData.element = '???';
	# 			}

	# 			this.moveHit(target, posData.source, move, posData.moveData);

	# 			this.effectData.positions[i] = null;
	# 		}
	# 		if (finished) {
	# 			side.removeSideCondition('futuremove');
	# 		}
	# 	}
	# },
	# stall: {
	# 	// Protect, Detect, Endure counter
	# 	duration: 2,
	# 	counterMax: 729,
	# 	onStart: function () {
	# 		this.effectData.counter = 3;
	# 	},
	# 	onStallMove: function () {
	# 		// this.effectData.counter should never be undefined here.
	# 		// However, just in case, use 1 if it is undefined.
	# 		var counter = this.effectData.counter || 1;
	# 		this.debug("Success chance: " + Math.round(100 / counter) + "%");
	# 		return (this.random(counter) === 0);
	# 	},
	# 	onRestart: function () {
	# 		if (this.effectData.counter < this.effect.counterMax) {
	# 			this.effectData.counter *= 3;
	# 		}
	# 		this.effectData.duration = 2;
	# 	}
	# },
	# gem: {
	# 	duration: 1,
	# 	affectsFainted: true,
	# 	onBasePower: function (basePower, user, target, move) {
	# 		this.debug('Gem Boost');
	# 		return this.chainModify([0x14CD, 0x1000]);
	# 	}
	# },
	# aura: {
	# 	duration: 1,
	# 	onBasePowerPriority: 8,
	# 	onBasePower: function (basePower, user, target, move) {
	# 		var modifier = 0x1547;
	# 		this.debug('Aura Boost');
	# 		if (user.volatiles['aurabreak']) {
	# 			modifier = 0x0C00;
	# 			this.debug('Aura Boost reverted by Aura Break');
	# 		}
	# 		return this.chainModify([modifier, 0x1000]);
	# 	}
	# },

	# weather is implemented here since it's so important to the game

def RAINDANCEonStart(source):
	weather.set_weather(weather.RAINDANCE, 5)
	if (source and source.item == "DAMPROCK"):
		weather.set_weather(weather.RAINDANCE, 8)
	if (source.ability == "DRIZZLE"):
		weather.set_weather(weather.RAINDANCE, -1)
def RAINDANCEonBasePower(basePower, attacker, defender, move):
	if (move.element == "WATER"):
		return 1.5 * basePower
	if (move.element == "FIRE"):
		return 0.5 * basePower
def RAINDANCEonResidual():
	weather.decrement_weather()
def RAINDANCEonEnd():
	if (weather.get_weather_countdown() == 0):
		weather.clear_weather()
	# primordialsea: {
	# 	effectType: 'Weather',
	# 	duration: 0,
	# 	onTryMove: function (target, source, effect) {
	# 		if (effect.element === 'Fire' && effect.category !== 'Status') {
	# 			this.debug('Primordial Sea fire suppress');
	# 			this.add('-fail', source, effect, '[from] Primordial Sea');
	# 			return null;
	# 		}
	# 	},
	# 	onBasePower: function (basePower, attacker, defender, move) {
	# 		if (move.element === 'Water') {
	# 			this.debug('Rain water boost');
	# 			return this.chainModify(1.5);
	# 		}
	# 	},
	# 	onStart: function () {
	# 		this.add('-weather', 'PrimordialSea');
	# 	},
	# 	onResidualOrder: 1,
	# 	onResidual: function () {
	# 		this.add('-weather', 'PrimordialSea', '[upkeep]');
	# 		this.eachEvent('Weather');
	# 	},
	# 	onEnd: function () {
	# 		this.add('-weather', 'none');
	# 	}
	# },

def SUNNYDAYonStart(source):
	weather.set_weather(weather.SUNNYDAY, 5)
	if (source and source.item == "HEATROCK"):
		weather.set_weather(weather.SUNNYDAY, 8)
	if (source.ability == "DROUGHT"):
		weather.set_weather(weather.SUNNYDAY, -1)
def SUNNYDAYonBasePower(basePower, attacker, defender, move):
	if (move.element == "FIRE"):
		return basePower * 1.5
	if (move.element == "WATER"):
		return basePower * 0.5
def SUNNYDAYonImmunity(element): # not sure if this is necessary - took it from js version
	if (element == "ICE"):
		return False
def SUNNYDAYonResidual():
	weather.decrement_weather()
def SUNNYDAYonEnd():
	if (weather.get_weather_countdown() == 0):
		weather.clear_weather()
	# desolateland: {
	# 	effectType: 'Weather',
	# 	duration: 0,
	# 	onTryMove: function (target, source, effect) {
	# 		if (effect.element === 'Water' && effect.category !== 'Status') {
	# 			this.debug('Desolate Land water suppress');
	# 			this.add('-fail', source, effect, '[from] Desolate Land');
	# 			return null;
	# 		}
	# 	},
	# 	onBasePower: function (basePower, attacker, defender, move) {
	# 		if (move.element === 'Fire') {
	# 			this.debug('Sunny Day fire boost');
	# 			return this.chainModify(1.5);
	# 		}
	# 	},
	# 	onStart: function () {
	# 		this.add('-weather', 'DesolateLand');
	# 	},
	# 	onImmunity: function (element) {
	# 		if (element === 'frz') return false;
	# 	},
	# 	onResidualOrder: 1,
	# 	onResidual: function () {
	# 		this.add('-weather', 'DesolateLand', '[upkeep]');
	# 		this.eachEvent('Weather');
	# 	},
	# 	onEnd: function () {
	# 		this.add('-weather', 'none');
	# 	}
	# },
	# sandstorm: {
	# 	effectType: 'Weather',
	# 	duration: 5,
	# 	durationCallback: function (source, effect) {
	# 		if (source && source.hasItem('smoothrock')) {
	# 			return 8;
	# 		}
	# 		return 5;
	# 	},
	# 	// This should be applied directly to the stat before any of the other modifiers are chained
	# 	// So we give it increased priority.
	# 	onModifySpDPriority: 10,
	# 	onModifySpD: function (spd, pokemon) {
	# 		if (pokemon.hasType('Rock') && this.isWeather('sandstorm')) {
	# 			return this.modify(spd, 1.5);
	# 		}
	# 	},
	# 	onStart: function (battle, source, effect) {
	# 		if (effect && effect.effectType === 'Ability' && this.gen <= 5) {
	# 			this.effectData.duration = 0;
	# 			this.add('-weather', 'Sandstorm', '[from] ability: ' + effect, '[of] ' + source);
	# 		} else {
	# 			this.add('-weather', 'Sandstorm');
	# 		}
	# 	},
	# 	onResidualOrder: 1,
	# 	onResidual: function () {
	# 		this.add('-weather', 'Sandstorm', '[upkeep]');
	# 		if (this.isWeather('sandstorm')) this.eachEvent('Weather');
	# 	},
	# 	onWeather: function (target) {
	# 		this.damage(target.max_hp / 16);
	# 	},
	# 	onEnd: function () {
	# 		this.add('-weather', 'none');
	# 	}
	# },
	# hail: {
	# 	effectType: 'Weather',
	# 	duration: 5,
	# 	durationCallback: function (source, effect) {
	# 		if (source && source.hasItem('icyrock')) {
	# 			return 8;
	# 		}
	# 		return 5;
	# 	},
	# 	onStart: function (battle, source, effect) {
	# 		if (effect && effect.effectType === 'Ability' && this.gen <= 5) {
	# 			this.effectData.duration = 0;
	# 			this.add('-weather', 'Hail', '[from] ability: ' + effect, '[of] ' + source);
	# 		} else {
	# 			this.add('-weather', 'Hail');
	# 		}
	# 	},
	# 	onResidualOrder: 1,
	# 	onResidual: function () {
	# 		this.add('-weather', 'Hail', '[upkeep]');
	# 		if (this.isWeather('hail')) this.eachEvent('Weather');
	# 	},
	# 	onWeather: function (target) {
	# 		this.damage(target.max_hp / 16);
	# 	},
	# 	onEnd: function () {
	# 		this.add('-weather', 'none');
	# 	}
	# },
	# deltastream: {
	# 	effectType: 'Weather',
	# 	duration: 0,
	# 	onEffectiveness: function (elementMod, target, element, move) {
	# 		if (move && move.effectType === 'Move' && element === 'Flying' && elementMod > 0) {
	# 			this.add('-activate', '', 'deltastream');
	# 			return 0;
	# 		}
	# 	},
	# 	onStart: function () {
	# 		this.add('-weather', 'DeltaStream');
	# 	},
	# 	onResidualOrder: 1,
	# 	onResidual: function () {
	# 		this.add('-weather', 'DeltaStream', '[upkeep]');
	# 		this.eachEvent('Weather');
	# 	},
	# 	onEnd: function () {
	# 		this.add('-weather', 'none');
	# 	}
	# },

	# arceus: {
	# 	// Arceus's actual typing is implemented here
	# 	// Arceus's true typing for all its formes is Normal, and it's only
	# 	// Multielement that changes its element, but its formes are specified to
	# 	// be their corresponding element in the Pokedex, so that needs to be
	# 	// overridden. This is mainly relevant for Hackmons and Balanced
	# 	// Hackmons.
	# 	onSwitchInPriority: 101,
	# 	onSwitchIn: function (pokemon) {
	# 		var element = 'Normal';
	# 		if (pokemon.ability === 'multielement') {
	# 			element = pokemon.getItem().onPlate;
	# 			if (!element || element === true) {
	# 				element = 'Normal';
	# 			}
	# 		}
	# 		pokemon.setType(element, true);
	# 	}
	# }
def REFLECTonStart(source):
	source.reflect_countdown = 5
	if (source.item == "LIGHTCLAY"):
		source.reflect_countdown = 8
	if (source.add_volatile(REFLECT)):
		log.message("A wall of light appeared in front of " + source.template.species)
def REFLECTonModifyDamage(damage, source, target, move):
	if (target != source and move.category == "PHYSICAL"):
		return damage * 0.66
def REFLECTonEnd(pokemon):
	pokemon.reflect_countdown -= 1
	if (pokemon.reflect_countdown <= 0 and pokemon.remove_volatile(REFLECT)):
		log.message(pokemon.template.species + "'s Reflect faded")

battle_status = {
	"NONE" : BattleStatus("NONE", "STATUS"),
	"BRN" : BattleStatus("BRN", "STATUS", onStart = BRNonStart, onResidualOrder = 9, onResidual = BRNonResidual),
	"PAR" : BattleStatus("PAR", "STATUS", onStart = PARonStart, onBeforeMovePriority = 1, onBeforeMove = PARonBeforeMove),
	"SLP" : BattleStatus("SLP", "STATUS", onStart = SLPonStart, onBeforeMovePriority = 10, onBeforeMove = SLPonBeforeMove),
	"FRZ" : BattleStatus("FRZ", "STATUS", onStart = FRZonStart, onBeforeMovePriority = 10, onBeforeMove = FRZonBeforeMove, onHit = FRZonHit),#, onModifyMove = FRZonModifyMove),
	"PSN" : BattleStatus("PSN", "STATUS", onStart = PSNonStart, onResidualOrder = 9, onResidual = PSNonResidual),
	"TOX" : BattleStatus("TOX", "STATUS", onStart = TOXonStart, onSwitchIn = TOXonSwitchIn, onResidualOrder = 9, onResidual = TOXonResidual),
	"CONFUSION" : BattleStatus("CONFUSION", "VOLATILE", onStart = CONFUSIONonStart, onBeforeMovePriority = 3, onBeforeMove = CONFUSIONonBeforeMove),#, onEnd = CONFUSIONonEnd),
	"FLINCH" : BattleStatus("FLINCH", "VOLATILE", onBeforeMovePriority = 8, onBeforeMove = FLINCHonBeforeMove),
	# "TRAPPED" : BattleStatus("TRAPPED", "VOLATILE", noCopy = True, onTrySwitchAction = TRAPPEDonTrySwitchAction, onStart = TRAPPEDonStart),
	# "TRAPPER" : BattleStatus("TRAPPER", "VOLATILE", noCopy = True),
	"PARTIALLYTRAPPED" : BattleStatus("PARTIALLYTRAPPED", "VOLATILE", onStart = PARTIALLYTRAPPEDonStart, onResidualOrder = 11, onResidual = PARTIALLYTRAPPEDonResidual, onTrySwitchAction = PARTIALLYTRAPPEDonTrySwitchAction),#, onEnd = PARTIALLYTRAPPEDonEnd),
	# "LOCKEDMOVE" : BattleStatus("LOCKEDMOVE", "VOLATILE", onResidual = LOCKEDMOVEonResidual, onStart = LOCKEDMOVEonRestart, onRestart = LOCKEDMOVEonRestart, onEnd = LOCKEDMOVEonEnd, onLockMove = LOCKEDMOVEonLockMove),
	"TWOTURNMOVE" : BattleStatus("TWOTURNMOVE", "VOLATILE", onStart = TWOTURNMOVEonStart, onEnd = TWOTURNMOVEonEnd),#, onLockMove = TWOTURNMOVEonLockMove, onLockMoveTarget = TWOTURNMOVEonLockMoveTarget),
	# "CHOICELOCK" : BattleStatus("CHOICELOCK", "VOLATILE", onStart = CHOICELOCKonStart, onDisableMove = CHOICELOCKonDisableMove),
	# "MUSTRECHARGE" : BattleStatus("MUSTRECHARGE", "VOLATILE", onBeforeMovePriority = 11, onBeforeMove = MUSTRECHARGEonBeforeMove, onLockMove = MUSTRECHARGEonLockMove),
	# "FUTUREMOVE" : BattleStatus("FUTUREMOVE", "VOLATILE", onStart = FUTUREMOVEonStart, onResidualOrder = 3, onResidual = FUTUREMOVEonResidual),
	# "STALL" : BattleStatus("STALL", "VOLATILE", onStart = STALLonStart, onStallMove = STALLonStallMove, onRestart = STALLonRestart),
	# "GEM" : BattleStatus("GEM", "VOLATILE", onBasePower = GEMonBasePower),
	# "AURA" : BattleStatus("AURA", "VOLATILE", onBasePowerPriority = 8, onBasePower = AURAonBasePower),
	"RAINDANCE" : BattleStatus("RAINDANCE", "WEATHER", onStart = RAINDANCEonStart, onBasePower = RAINDANCEonBasePower, onResidualOrder = 1, onResidual = RAINDANCEonResidual, onEnd = RAINDANCEonEnd),
	# "PRIMORDIALSEA" : BattleStatus("PRIMORDIALSEA", "WEATHER", onTryMove = PRIMORDIALSEAonTryMove, onBasePower = PRIMORDIALSEAonBasePower, onStart = PRIMORDIALSEAonStart, onResidualOrder = 1, onResidual = PRIMORDIALSEAonResidual, onEnd = PRIMORDIALSEAonEnd),
	"SUNNYDAY" : BattleStatus("SUNNYDAY", "WEATHER", onBasePower = SUNNYDAYonBasePower, onStart = SUNNYDAYonStart, onImmunity = SUNNYDAYonImmunity, onResidualOrder = 1, onResidual = SUNNYDAYonResidual, onEnd = SUNNYDAYonEnd),
	# "DESOLATELAND" : BattleStatus("DESOLATELAND", "WEATHER", onTryMove = DESOLATELANDonTryMove, onBasePower = DESOLATELANDonBasePower, onStart = DESOLATELANDonStart, onImmunity = DESOLATELANDonImmunity, onResidualOrder = 1, onResidual = DESOLATELANDonResidual, onEnd = DESOLATELANDonEnd),
	# "SANDSTORM" : BattleStatus("SANDSTORM", "WEATHER", onModifySpDPriority = 10, onModifySpD = SANDSTORMonModifySpD, onStart = SANDSTORMonStart, onResidualOrder = 1, onResidual = SANDSTORMonResidual, onWeather = SANDSTORMonWeather, onEnd = SANDSTORMonEnd),
	# "HAIL" : BattleStatus("HAIL", "WEATHER", onStart = HAILonStart, onResidualOrder = 1, onResidual = HAILonResidual, onWeather = HAILonWeather, onEnd = HAILonEnd),
	# "DELTASTREAM" : BattleStatus("DELTASTREAM", "WEATHER", onEffectiveness = DELTASTREAMonEffectiveness, onStart = DELTASTREAMonStart, onResidualOrder = 1, onResidual = DELTASTREAMonResidual, onEnd = DELTASTREAMonEnd),
	# "ARCEUS" : BattleStatus("ARCEUS", "", onSwitchInPriority = 101, onSwitchIn = ARCEUSonSwitchIn),
	"REFLECT" : BattleStatus("REFLECT", "VOLATILE", onStart = REFLECTonStart, onModifyDamage = REFLECTonModifyDamage, onResidualOrder = 21, onEnd = REFLECTonEnd), # may not need onResidualOrder (taken from javascript),
}