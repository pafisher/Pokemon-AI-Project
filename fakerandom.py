import random

random.seed(1)

def fakerandom():
	return random.random()

def fakerandint(a, b):
	return random.randint(a, b)

def fakechoice(some_list):
	return random.choice(some_list)