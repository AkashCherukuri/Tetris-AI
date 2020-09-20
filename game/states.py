from enum import Enum
import random

class State(Enum):
	GAME_START = 0
	GAME_CONT = 1
	GAME_END = 2

class Move(Enum):
	Down = 0
	Left = 1
	Right = 2
	Rotate = 3

class Pc(Enum):
	I=0; O=1; T=2; S=3; Z=4; J=5; L=6;

class PcR(Enum):
	I1=0; I2 = 0.5;
	O=1; 
	T1=2; T2=2.1; T3=2.2; T4=2.3; 
	S1=3; S2=3.1; 
	Z1=4; Z2=4.1; 
	J1=5; J2=5.1; J3=5.2; J4=5.3; 
	L1=6; L2=6.1; L3=6.2; L4=6.3;

class Gen_P:
	def __init__(self):
		self.bag = []

	def give(self):
		if(len(self.bag) == 0):
			self.bag = [Pc.I, Pc.O, Pc.T, Pc.S, Pc.Z, Pc.J, Pc.L
								  ]
			random.shuffle(self.bag)
		a = self.bag.pop()
		return a