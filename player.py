import status
import fakerandom

# actions
SWITCH = "SWITCH"
ATTACK = "ATTACK"

class Action:
	def __init__(self, action, user, target = None):
		self.action = action
		self.user = user
		self.target = target

class Player:
	def __init__(self, ID):
		self.ID = ID
	def get_id(self):
		return self.ID
	def set_team(self, team):
		self.team = team
	def get_action(self, battle):
		pass
	def set_active(self, pokemon):
		self.active = pokemon
	def get_fainted_switch(self, battle):
		pass

class RandomAI(Player):
	def __init__(self, ID):
		self.ID = ID
	def get_id(self):
		return self.ID
	def get_action(self, battle):
		print ("Choose an action: " + str(self.get_id()))
		print ("Opponent")
		opponent_decision_vars = None
		if (battle.active1 == self.active):
			opponent_decision_vars = battle.active2.get_decision_vars()
			opponent_decision_vars.print_min_decision_vars()
		else:
			opponent_decision_vars = battle.active1.get_decision_vars()
			opponent_decision_vars.print_min_decision_vars()
		print ("Active Pokemon")
		active_decision_vars = self.active.get_decision_vars()
		active_decision_vars.print_min_decision_vars()
		print ("Team")
		for pokemon in self.team.pokemon:
			if (pokemon.fainted == False and pokemon.is_active == False):
				decision_vars = pokemon.get_decision_vars()
				decision_vars.print_min_decision_vars()
		while True:
			possible_choices = []
			for pokemon in self.team.pokemon:
				if (pokemon.fainted == False and pokemon.is_active == False):
					possible_choices.append(Action(SWITCH, self.active, pokemon))
			for move in self.active.moves:
				if (move.pp > 0):
					possible_choices.append(Action(ATTACK, self.active, move))
					possible_choices.append(Action(ATTACK, self.active, move))
					possible_choices.append(Action(ATTACK, self.active, move))
			return fakerandom.fakechoice(possible_choices)
	def set_active(self, pokemon):
		self.active = pokemon
	def get_fainted_switch(self, battle):
		print (str(self.get_id()) + ": Your active Pokemon fainted, choose a Pokemon to switch in")
		print ("Opponent")
		opponent_decision_vars = None
		if (battle.active1 == self.active):
			opponent_decision_vars = battle.active2.get_decision_vars()
			opponent_decision_vars.print_min_decision_vars()
		else:
			opponent_decision_vars = battle.active1.get_decision_vars()
			opponent_decision_vars.print_min_decision_vars()
		print ("Team")
		for pokemon in self.team.pokemon:
			if (pokemon.fainted == False):
				decision_vars = pokemon.get_decision_vars()
				decision_vars.print_min_decision_vars()
		while True:
			possible_choices = []
			for pokemon in self.team.pokemon:
				if (pokemon.fainted == False):
					possible_choices.append(pokemon)
			return fakerandom.fakechoice(possible_choices)

class HumanPlayer(Player):
	def __init__(self, ID):
		self.ID = ID
	def get_id(self):
		return self.ID
	def get_action(self, battle):
		print ("\n\nChoose an action: " + str(self.get_id()))
		print ("\n\nOpponent")
		opponent_decision_vars = None
		if (battle.active1 == self.active):
			opponent_decision_vars = battle.active2.get_decision_vars()
			opponent_decision_vars.print_opponent_decision_vars()
		else:
			opponent_decision_vars = battle.active1.get_decision_vars()
			opponent_decision_vars.print_opponent_decision_vars()
		print ("\n\nActive Pokemon")
		active_decision_vars = self.active.get_decision_vars()
		active_decision_vars.print_full_decision_vars()
		print ("\n\nTeam")
		for pokemon in self.team.pokemon:
			if (pokemon.fainted == False and pokemon.is_active == False):
				decision_vars = pokemon.get_decision_vars()
				decision_vars.print_team_decision_vars()
				print ("\n")
		while True:
			choice = raw_input("Type Pokemon name to switch to that Pokemon or move name to use that move: ")
			for pokemon in self.team.pokemon:
				if (pokemon.fainted == False and pokemon.template.species == choice and pokemon.is_active == False):
					return Action(SWITCH, self.active, pokemon)
			for move in self.active.moves:
				if (move.pp > 0 and move.name == choice):
					return Action(ATTACK, self.active, move)
	def set_active(self, pokemon):
		self.active = pokemon
	def get_fainted_switch(self, battle):
		print (str(self.get_id()) + ": Your active Pokemon fainted, choose a Pokemon to switch in")
		print ("\n\nOpponent")
		opponent_decision_vars = None
		if (battle.active1 == self.active):
			opponent_decision_vars = battle.active2.get_decision_vars()
			opponent_decision_vars.print_opponent_decision_vars()
		else:
			opponent_decision_vars = battle.active1.get_decision_vars()
			opponent_decision_vars.print_opponent_decision_vars()
		print ("\n\nTeam")
		for pokemon in self.team.pokemon:
			if (pokemon.fainted == False):
				decision_vars = pokemon.get_decision_vars()
				decision_vars.print_team_decision_vars()
				print ("\n")
		while True:
			choice = raw_input("Type Pokemon name to switch to that Pokemon: ")
			for pokemon in self.team.pokemon:
				if (pokemon.fainted == False and pokemon.template.species == choice):
					return pokemon

class LearningAI(Player):
	def __init__(self, ID):
		self.ID = ID
	def get_id(self):
		return self.ID
	def get_action(self, battle):
		pass
	def set_active(self, pokemon):
		self.active = pokemon
	def get_fainted_switch(self, battle):
		pass