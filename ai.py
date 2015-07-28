class PokemonDecisionVars:
	def __init__(self, fainted, template, max_hp, hp, status, volatiles, atk_stage, def_stage, spa_stage, spd_stage, spe_stage, acc_stage, eva_stage, crit_stage, moves):
		self.fainted = fainted
		self.template = template
		self.max_hp = max_hp
		self.hp = hp
		self.status = status
		self.volatiles = volatiles
		self.atk_stage = atk_stage
		self.def_stage = def_stage
		self.spa_stage = spa_stage
		self.spd_stage = spd_stage
		self.spe_stage = spe_stage
		self.acc_stage = acc_stage
		self.eva_stage = eva_stage
		self.crit_stage = crit_stage
		self.move1 = moves[0]
		self.move2 = moves[1]
		self.move3 = moves[2]
		self.move4 = moves[3]
	def print_full_decision_vars(self):
		print "self.species: " + str(self.template.species)
		print "self.elements: " + str(self.template.elements)
		print "self.max_hp: " + str(self.max_hp)
		print "self.hp: " + str(self.hp)
		if (self.status.name != "NONE"):
			print "self.status: " + str(self.status.name)
		if (self.volatiles != []):
			print "self.volatiles: " + str(self.volatiles)
		if (self.atk_stage != 0):
			print "self.atk_stage: " + str(self.atk_stage)
		if (self.def_stage != 0):
			print "self.def_stage: " + str(self.def_stage)
		if (self.spa_stage != 0):
			print "self.spa_stage: " + str(self.spa_stage)
		if (self.spd_stage != 0):
			print "self.spd_stage: " + str(self.spd_stage)
		if (self.spe_stage != 0):
			print "self.spe_stage: " + str(self.spe_stage)
		if (self.acc_stage != 0):
			print "self.acc_stage: " + str(self.acc_stage)
		if (self.eva_stage != 0):
			print "self.eva_stage: " + str(self.eva_stage)
		if (self.crit_stage != 0):
			print "self.crit_stage: " + str(self.crit_stage)
		print "self.move1: " + str(self.move1.name) + " pp: " + str(self.move1.pp) + "\t\tself.move2: " + str(self.move2.name) + " pp: " + str(self.move2.pp) + "\t\tself.move3: " + str(self.move3.name) + " pp: " + str(self.move3.pp) + "\t\tself.move4: " + str(self.move4.name) + " pp: " + str(self.move4.pp)
	def print_opponent_decision_vars(self):
		print "self.species: " + str(self.template.species)
		print "self.elements: " + str(self.template.elements)
		print "self.max_hp: " + str(self.max_hp)
		print "self.hp: " + str(self.hp)
		if (self.status.name != "NONE"):
			print "self.status: " + str(self.status.name)
		if (self.volatiles != []):
			print "self.volatiles: " + str(self.volatiles)
		if (self.atk_stage != 0):
			print "self.atk_stage: " + str(self.atk_stage)
		if (self.def_stage != 0):
			print "self.def_stage: " + str(self.def_stage)
		if (self.spa_stage != 0):
			print "self.spa_stage: " + str(self.spa_stage)
		if (self.spd_stage != 0):
			print "self.spd_stage: " + str(self.spd_stage)
		if (self.spe_stage != 0):
			print "self.spe_stage: " + str(self.spe_stage)
		if (self.acc_stage != 0):
			print "self.acc_stage: " + str(self.acc_stage)
		if (self.eva_stage != 0):
			print "self.eva_stage: " + str(self.eva_stage)
		if (self.crit_stage != 0):
			print "self.crit_stage: " + str(self.crit_stage)
	def print_team_decision_vars(self):
		print "self.species: " + str(self.template.species)
		print "self.elements: " + str(self.template.elements)
		print "self.max_hp: " + str(self.max_hp)
		print "self.hp: " + str(self.hp)
		if (self.status.name != "NONE"):
			print "self.status: " + str(self.status.name)
		print "self.move1: " + str(self.move1.name) + " pp: " + str(self.move1.pp) + "\t\tself.move2: " + str(self.move2.name) + " pp: " + str(self.move2.pp) + "\t\tself.move3: " + str(self.move3.name) + " pp: " + str(self.move3.pp) + "\t\tself.move4: " + str(self.move4.name) + " pp: " + str(self.move4.pp)
	def print_min_decision_vars(self):
		print "self.species: " + str(self.template.species)
		print "self.hp: " + str(self.hp)