from enum import Enum
import random

class State(Enum):
	GAME_START = 0
	GAME_CONT = 1
	GAME_END = 2

class Pc(Enum):
	I=0; O=1; #T=2; S=3; Z=4; J=5; L=6;

class Gen_P:
	def __init__(self):
		self.bag = []

	def give(self):
		if(len(self.bag) == 0):
			self.bag = [Pc.I, Pc.O#, Pc.T, Pc.S, Pc.Z, Pc.J, Pc.L
								  ]
			random.shuffle(self.bag)
		a = self.bag.pop()
		return a