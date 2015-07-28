import pokedex
import moves
import copy
import learnsets
import natures
import debug
import status
import ai
import log
dbflag = True

ATK = "ATK"
DEF = "DEF"
SPA = "SPA"
SPD = "SPD"
SPE = "SPE"
ACC = "ACC"
EVA = "EVA"

def get_hp_element(ivs):
	hp_element = int(((ivs[0] % 2 + 2 * (ivs[1] % 2) + 4 * (ivs[2] % 2) + 8 * (ivs[5] % 2) + 16 * (ivs[3] % 2) + 32 * (ivs[4] % 2)) * 15) / 63)
	if (hp_element == 0):
		return "FIGHTING"
	if (hp_element == 1):
		return "FLYING"
	if (hp_element == 2):
		return "POISON"
	if (hp_element == 3):
		return "GROUND"
	if (hp_element == 4):
		return "ROCK"
	if (hp_element == 5):
		return "BUG"
	if (hp_element == 6):
		return "GHOST"
	if (hp_element == 7):
		return "STEEL"
	if (hp_element == 8):
		return "FIRE"
	if (hp_element == 9):
		return "WATER"
	if (hp_element == 10):
		return "GRASS"
	if (hp_element == 11):
		return "ELECTRIC"
	if (hp_element == 12):
		return "PSYCHIC"
	if (hp_element == 13):
		return "ICE"
	if (hp_element == 14):
		return "DRAGON"
	if (hp_element == 15):
		return "DARK"

class Pokemon:
	def __init__(self, species, level, ivs, evs, techniques, nature, gender, ability, item): # had to rename init variable "moves" to "techniques" to solve a naming conflict
		self.template = pokedex.pokedex_list[species]
		self.level = level
		self.nature = nature
		self.nature_dict = natures.nature_list[nature]
		self.max_hp = int((((ivs[0] + (2 * self.template.base_hp) + int(evs[0] / 4) + 100) * level) / 100) + 10)
		self.hp = self.max_hp
		self.attack = int(((((ivs[1] + (2 * self.template.base_atk) + int(evs[1] / 4)) * level) / 100) + 5) * self.nature_dict["ATK"])
		self.defence = int(((((ivs[2] + (2 * self.template.base_def) + int(evs[2] / 4)) * level) / 100) + 5) * self.nature_dict["DEF"])
		self.spattack = int(((((ivs[3] + (2 * self.template.base_spa) + int(evs[3] / 4)) * level) / 100) + 5) * self.nature_dict["SPA"])
		self.spdefence = int(((((ivs[4] + (2 * self.template.base_spd) + int(evs[4] / 4)) * level) / 100) + 5) * self.nature_dict["SPD"])
		self.speed = int(((((ivs[5] + (2 * self.template.base_spe) + int(evs[5] / 4)) * level) / 100) + 5) * self.nature_dict["SPE"])
		
		self.atk_stage = 0
		self.def_stage = 0
		self.spa_stage = 0
		self.spd_stage = 0
		self.spe_stage = 0

		self.acc_stage = 0
		self.eva_stage = 0
		self.crit_stage = 0

		self.status = status.battle_status["NONE"]
		self.status_source = None

		self.gender = gender
		self.ability = ability
		self.item = item

		self.trapped = False
		self.maybe_trapped = False
		self.maybe_disabled = False
		self.illusion = None
		self.fainted = False
		self.faint_queued = False
		self.last_item = ""
		self.ate_berry = False
		self.position = 0
		self.last_move = ""
		self.move_this_turn = ""
		self.last_damage = 0
		self.last_attacked_by = None
		self.used_item_this_turn = False
		self.newly_switched = False
		self.being_called_back = False
		self.is_active = False
		self.is_started = False # has this pokemon's Start events run yet?
		self.transformed = False
		self.during_move = False
		self.hp_element = get_hp_element(ivs)
		self.hp_power = 60

		self.moves = [None, None, None, None]
		self.moves[0] = copy.deepcopy(moves.battle_move[techniques[0][0]])
		self.moves[0].pp += int(self.moves[0].pp * techniques[0][1] * 0.2)
		self.moves[1] = copy.deepcopy(moves.battle_move[techniques[1][0]])
		self.moves[1].pp += int(self.moves[1].pp * techniques[1][1] * 0.2)
		self.moves[2] = copy.deepcopy(moves.battle_move[techniques[2][0]])
		self.moves[2].pp += int(self.moves[2].pp * techniques[2][1] * 0.2)
		self.moves[3] = copy.deepcopy(moves.battle_move[techniques[3][0]])
		self.moves[3].pp += int(self.moves[3].pp * techniques[3][1] * 0.2)

		self.status_counter = 0
		self.volatiles = []
		self.twoturnmove_source = None
		partiallytrapped_count = 0
		partiallytrapped_source = None
		reflect_countdown = 0

	def add_volatile(self, new_volatile, source = None):
		retval = False
		volatile = status.battle_status[new_volatile]
		if (not volatile in self.volatiles):
			self.volatiles.append(volatile)
			retval = True
		if (volatile.name == status.TWOTURNMOVE):
			self.twoturnmove_source = source
		return retval
	def remove_volatile(self, old_volatile):
		retval = False
		volatile = status.battle_status[old_volatile]
		if (volatile in self.volatiles):
			self.volatiles.remove(volatile)
			retval = True
		if (volatile.name == status.TWOTURNMOVE):
			self.twoturnmove_source = None
		return retval
	def damage(self, amount):
		self.hp = max(self.hp - amount, 0)
		if (self.hp == 0):
			self.fainted = True
	def heal(self, amount):
		log.message (self.template.species + " was healed")
		self.hp = min(self.hp + amount, self.max_hp)
	def set_status(self, new_status, force = False):
		st = status.battle_status[new_status]
		if (force):
			self.status = st
			return True
		else:
			if (self.status != status.battle_status["NONE"]):
				return False
			self.status = st
			return True
	def set_status_counter(self, amount):
		self.status_counter = amount
	def get_status_counter(self):
		return self.status_counter
	def increment_status_counter(self):
		self.status_counter += 1
	def decrement_status_counter(self):
		self.status_counter -= 1
	def cure_status(self):
		self.status = status.battle_status["NONE"]
	def try_trap(self):
		return "PARTIALLYTRAPPED" in self.volatiles and partiallytrapped_source.fainted == False
	def increment_atk(self, amount):
		if (amount > 0):
			if (self.atk_stage == 6):
				return False
			else:
				log.message(self.template.species + "'s attack rose")
				self.atk_stage = min(self.atk_stage + amount, 6)
		else:
			if (self.atk_stage == -6):
				return False
			else:
				log.message(self.template.species + "'s attack fell")
				self.atk_stage = max(self.atk_stage + amount, -6)
	def increment_def(self, amount):
		if (amount > 0):
			if (self.def_stage == 6):
				return False
			else:
				log.message(self.template.species + "'s defence rose")
				self.def_stage = min(self.def_stage + amount, 6)
		else:
			if (self.def_stage == -6):
				return False
			else:
				log.message(self.template.species + "'s defence fell")
				self.def_stage = max(self.def_stage + amount, -6)
	def increment_spa(self, amount):
		if (amount > 0):
			if (self.spa_stage == 6):
				return False
			else:
				log.message(self.template.species + "'s special attack rose")
				self.spa_stage = min(self.spa_stage + amount, 6)
		else:
			if (self.spa_stage == -6):
				return False
			else:
				log.message(self.template.species + "'s special attack fell")
				self.spa_stage = max(self.spa_stage + amount, -6)
	def increment_spd(self, amount):
		if (amount > 0):
			if (self.spd_stage == 6):
				return False
			else:
				log.message(self.template.species + "'s special defence rose")
				self.spd_stage = min(self.spd_stage + amount, 6)
		else:
			if (self.spd_stage == -6):
				return False
			else:
				log.message(self.template.species + "'s special defence fell")
				self.spd_stage = max(self.spd_stage + amount, -6)
	def increment_spe(self, amount):
		if (amount > 0):
			if (self.spe_stage == 6):
				return False
			else:
				log.message(self.template.species + "'s speed rose")
				self.spe_stage = min(self.spe_stage + amount, 6)
		else:
			if (self.spe_stage == -6):
				return False
			else:
				log.message(self.template.species + "'s speed fell")
				self.spe_stage = max(self.spe_stage + amount, -6)
	def increment_acc(self, amount):
		if (amount > 0):
			if (self.acc_stage == 6):
				return False
			else:
				log.message(self.template.species + "'s accuracy rose")
				self.acc_stage = min(self.acc_stage + amount, 6)
		else:
			if (self.acc_stage == -6):
				return False
			else:
				log.message(self.template.species + "'s accuracy fell")
				self.acc_stage = max(self.acc_stage + amount, -6)
	def increment_eva(self, amount):
		if (amount > 0):
			if (self.eva_stage == 6):
				return False
			else:
				log.message(self.template.species + "'s evasiveness rose")
				self.eva_stage = min(self.eva_stage + amount, 6)
		else:
			if (self.eva_stage == -6):
				return False
			else:
				log.message(self.template.species + "'s evasiveness fell")
				self.eva_stage = max(self.eva_stage + amount, -6)
	def get_stab(self, move_element):
		for elem in self.template.elements:
			if (move_element == elem):
				return 1.5
		return 1

	def get_decision_vars(self):
		return ai.PokemonDecisionVars(self.fainted, self.template, self.max_hp, self.hp, self.status, self.volatiles, self.atk_stage, self.def_stage, self.spa_stage, self.spd_stage, self.spe_stage, self.acc_stage, self.eva_stage, self.crit_stage, self.moves)

def get_pokemon_from_list(pokemonlist):
	species = ""
	level = 0
	hpiv = 0
	atkiv = 0
	defiv = 0
	spaiv = 0
	spdiv = 0
	speiv = 0
	hpev = 0
	atkev = 0
	defev = 0
	spaev = 0
	spdev = 0
	speev = 0
	atk1 = ""
	ppup1 = 0
	atk2 = ""
	ppup2 = 0
	atk3 = ""
	ppup3 = 0
	atk4 = ""
	ppup4 = 0
	nature = ""
	gender = None
	ability = ""
	item = None
	for line in pokemonlist:
		formattedline = line.strip()
		if (formattedline[:6] == "[HPIV]"):
			hpiv = int(formattedline[6:])
			if (0 > hpiv > 31):
				debug.db(dbflag, "HPIV: " + str(hpiv) + " out of range for " + species)
				return None
		elif (formattedline[:6] == "[HPEV]"):
			hpev = int(formattedline[6:])
			if (0 > hpev > 255):
				debug.db(dbflag, "HPEV: " + str(hpev) + " out of range " + species)
				return None
		elif (formattedline[:6] == "[ATKEV]"):
			atkev = int(formattedline[6:])
			if (0 > atkev > 255):
				debug.db(dbflag, "ATKEV: " + str(atkev) + " out of range " + species)
				return None
		elif (formattedline[:6] == "[DEFEV]"):
			defev = int(formattedline[6:])
			if (0 > defev > 255):
				debug.db(dbflag, "DEFEV: " + str(defev) + " out of range " + species)
				return None
		elif (formattedline[:6] == "[SPAEV]"):
			spaev = int(formattedline[6:])
			if (0 > spaev > 255):
				debug.db(dbflag, "SPAEV: " + str(spaev) + " out of range " + species)
				return None
		elif (formattedline[:6] == "[SPDEV]"):
			spdev = int(formattedline[6:])
			if (0 > spdev > 255):
				debug.db(dbflag, "SPDEV: " + str(spdev) + " out of range " + species)
				return None
		elif (formattedline[:6] == "[SPEEV]"):
			speev = int(formattedline[6:])
			if (0 > speev > 255):
				debug.db(dbflag, "SPEEV: " + str(speev) + " out of range " + species)
				return None
		elif (formattedline[:6] == "[ATK1]"):
			atk1 = formattedline[6:]
			if (not atk1 in learnsets.learnset_list[species]):
				debug.db(dbflag, atk1 + " is not a valid move for " + species)
				return None
		elif (formattedline[:6] == "[ATK2]"):
			atk2 = formattedline[6:]
			if (not atk2 in learnsets.learnset_list[species]):
				debug.db(dbflag, atk2 + " is not a valid move for " + species)
				return None
		elif (formattedline[:6] == "[ATK3]"):
			atk3 = formattedline[6:]
			if (not atk3 in learnsets.learnset_list[species]):
				debug.db(dbflag, atk3 + " is not a valid move for " + species)
				return None
		elif (formattedline[:6] == "[ATK4]"):
			atk4 = formattedline[6:]
			if (not atk4 in learnsets.learnset_list[species]):
				debug.db(dbflag, atk4 + " is not a valid move for " + species)
				return None
		elif (formattedline[:6] == "[ITEM]"):
			if (formattedline[6:] == "NONE"):
				item = None
			else:
				item = formattedline[6:]
		elif (formattedline[:7] == "[ATKIV]"):
			atkiv = int(formattedline[7:])
			if (0 > atkiv > 31):
				debug.db(dbflag, "ATKIV: " + str(atkiv) + " out of range for " + species)
				return None
		elif (formattedline[:7] == "[DEFIV]"):
			defiv = int(formattedline[7:])
			if (0 > defiv > 31):
				debug.db(dbflag, "DEFIV: " + str(defiv) + " out of range for " + species)
				return None
		elif (formattedline[:7] == "[SPAIV]"):
			spaiv = int(formattedline[7:])
			if (0 > spaiv > 31):
				debug.db(dbflag, "SPAIV: " + str(spaiv) + " out of range for " + species)
				return None
		elif (formattedline[:7] == "[SPDIV]"):
			spdiv = int(formattedline[7:])
			if (0 > spdiv > 31):
				debug.db(dbflag, "SPDIV: " + str(spdiv) + " out of range for " + species)
				return None
		elif (formattedline[:7] == "[SPEIV]"):
			speiv = int(formattedline[7:])
			if (0 > speiv > 31):
				debug.db(dbflag, "SPEIV: " + str(speiv) + " out of range for " + species)
				return None
		elif (formattedline[:7] == "[LEVEL]"):
			level = int(formattedline[7:])
			if (1 > level > 100):
				debug.db(dbflag, "LEVEL " + str(level) + " is out of range for " + species)
				return None
		elif (formattedline[:7] == "[PPUP1]"):
			ppup1 = int(formattedline[7:])
			if (0 > ppup1 > 3):
				debug.db(dbflag, "PPUP1 " + str(ppup1) + " is out of range for move1 for " + species)
				return None
		elif (formattedline[:7] == "[PPUP2]"):
			ppup2 = int(formattedline[7:])
			if (0 > ppup2 > 3):
				debug.db(dbflag, "PPUP2 " + str(ppup2) + " is out of range for move2 for " + species)
				return None
		elif (formattedline[:7] == "[PPUP3]"):
			ppup3 = int(formattedline[7:])
			if (0 > ppup3 > 3):
				debug.db(dbflag, "PPUP3 " + str(ppup3) + " is out of range for move3 for " + species)
				return None
		elif (formattedline[:7] == "[PPUP4]"):
			ppup4 = int(formattedline[7:])
			if (0 > ppup4 > 3):
				debug.db(dbflag, "PPUP4 " + str(ppup4) + " is out of range for move4 for " + species)
				return None
		elif (formattedline[:8] == "[NATURE]"):
			nature = formattedline[8:]
		elif (formattedline[:8] == "[GENDER]"):
			if (formattedline[8:] == "NONE"):
				gender = None
			else:
				gender = formattedline[8:]
		elif (formattedline[:9] == "[ABILITY]"):
			ability = formattedline[9:]
		elif (formattedline[:9] == "[SPECIES]"):
			species = formattedline[9:]
	if (hpev + atkev + defev + spaev + spdev + speev > 510):
		debug.db(dbflag, "EV total out of range for " + species)
		return None
	return Pokemon(species, level, [hpiv, atkiv, defiv, spaiv, spdiv, speiv], [hpev, atkev, defev, spaev, spdev, speev], [(atk1, ppup1), (atk2, ppup2), (atk3, ppup3), (atk4, ppup4)], nature, gender, ability, item)