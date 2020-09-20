from game.core import tetris
from game.states import PcR, Pc, State
import pygame, random, copy, time, numpy
from pygame.locals import *

class T_bot(tetris):
	def __init__(self):
		super().__init__()	

	def spawn_w_rot(self, new, arr = None):
		if arr is None:
			arr = self.playArray
		#Python has no switch statement lul; use dict-mapping maybe?
		if new is PcR.I1:
			for i in range((self.wd//2)-2, (self.wd//2)+2):
				if arr[0,i] == 1:
					return True
			for i in range((self.wd//2)-2, (self.wd//2)+2):
				arr[0,i] = 2

		elif new is PcR.I2:
			for j in range(4):
				if arr[j,self.wd//2] == 1:
					return True
			for j in range(4):
				arr[j, self.wd//2] = 2			

		elif new is PcR.O:
			for i in range((self.wd//2)-1, (self.wd//2)+1):
				if arr[1,i] == 1:
					return True
			for i in range((self.wd//2)-1, (self.wd//2)+1):
				arr[0,i] = 2
				arr[1,i] = 2

		elif new is PcR.T1 or new is PcR.J1 or new is PcR.L1:
			for i in range((self.wd//2)-1, (self.wd//2)+2):
				if arr[1,i] == 1:
					return True
			for i in range((self.wd//2)-1, (self.wd//2)+2):
				arr[1,i] = 2
			if new is PcR.J1:
				arr[0, (self.wd//2)-1] = 2
			elif new is PcR.T1:
				arr[0, (self.wd//2)] = 2
			else:
				arr[0, (self.wd//2)+1] = 2
	
		elif new is PcR.T3 or new is PcR.J3 or new is PcR.L3:
			for i in range((self.wd//2)-1, (self.wd//2)+2):
				if arr[1,i] == 1:				#OverChecking here, but if the ai got to that point, its pretty bad
					return True
			for i in range((self.wd//2)-1, (self.wd//2)+2):
				arr[0,i] = 2
			if new is PcR.J3:
				arr[1, (self.wd//2)-1] = 2
			elif new is PcR.T3:
				arr[1, (self.wd//2)] = 2
			else:
				arr[1, (self.wd//2)+1] = 2

		elif new is PcR.T2 or new is PcR.J2 or new is PcR.L2:
			for i in range((self.wd//2)-1, (self.wd//2)+1):	#OverChecking here, but if the ai got to that point, its pretty bad
				if arr[i,self.wd//2] == 1:
					return True
			for i in range(3):
				arr[i,self.wd//2] = 2
			if new is PcR.J2:
				arr[0, (self.wd//2)-1] = 2
			elif new is PcR.T2:
				arr[1, (self.wd//2)-1] = 2
			else:
				arr[2, (self.wd//2)-1] = 2

		elif new is PcR.T4 or new is PcR.J4 or new is PcR.L4:
			for i in range((self.wd//2)-1, (self.wd//2)+1):	#OverChecking here, but if the ai got to that point, its pretty bad
				if arr[i,self.wd//2] == 1:
					return True
			for i in range(3):
				arr[i,(self.wd//2)-1] = 2
			if new is PcR.J4:
				arr[0, (self.wd//2)] = 2
			elif new is PcR.T4:
				arr[1, (self.wd//2)] = 2
			else:
				arr[2, (self.wd//2)] = 2

		elif new is PcR.S1:
			for i in range((self.wd//2)-1, (self.wd//2)+1):
				if arr[1,i] == 1:
					return True
			arr[1, (self.wd//2)-1] = 2
			arr[1, (self.wd//2)] = 2
			arr[0, (self.wd//2)] = 2
			arr[0, (self.wd//2)+1] = 2

		elif new is PcR.S2:
			for i in range((self.wd//2)-1, (self.wd//2)+1):
				if arr[2,i] == 1:				#OverChecking!
					return True
			arr[0, (self.wd//2)-1] = 2
			arr[1, (self.wd//2)-1] = 2
			arr[1, (self.wd//2)] = 2
			arr[2, (self.wd//2)] = 2

		elif new is PcR.Z1:
			for i in range((self.wd//2), (self.wd//2)+2):
				if arr[1,i] == 1:
					return True
			arr[1, (self.wd//2)+1] = 2
			arr[1, (self.wd//2)] = 2
			arr[0, (self.wd//2)] = 2
			arr[0, (self.wd//2)-1] = 2			

		elif new is PcR.Z2:
			for i in range((self.wd//2), (self.wd//2)+2):
				if arr[1,i] == 1:				#OverChecking!
					return True
			arr[0, (self.wd//2)] = 2
			arr[1, (self.wd//2)] = 2
			arr[1, (self.wd//2)-1] = 2
			arr[2, (self.wd//2)-1] = 2			

		return False

	def hole_height(self, arr):
		if self.check_last(self.screen, arr) > 0:
			compl_rew = -50

		arr = numpy.transpose(arr)
		cnt = 0
		compl_rew = 0
		diff=[]; ho_val = []; tmp = []
		val = []

		for i in range(self.wd):
			tmp.append(numpy.trim_zeros(arr[i], 'f'))
			val.append(len(tmp[-1]))

			cnt = cnt + numpy.count_nonzero(tmp[-1]==0)			#This calc of holes is problematic

		for i in range(self.wd):
			for j in range(self.ht-1, self.ht-1-len(tmp[i]), -1):
				if i > 0 and i < (self.wd-1):
					if arr[i][j]==0 and arr[i-1][j]==1 and arr[i+1][j]==1:
						cnt+=4
				elif i == 0:
					if arr[i][j]==0 and arr[i+1][j]==1:
						cnt+=4
				elif i == self.wd-1:
					if arr[i][j]==0 and arr[i-1][j]==1:
						cnt+=4


		return (cnt, max(val), max(val)-min(val), compl_rew)

	def simulate_1(self, pc):
		poss = []
		if pc is Pc.I:
			poss.append(PcR.I1)
			poss.append(PcR.I2)
		elif pc is Pc.O:
			poss.append(PcR.O)
		elif pc is Pc.T:
			poss.append(PcR.T1)
			poss.append(PcR.T2)
			poss.append(PcR.T3)
			poss.append(PcR.T4)
		elif pc is Pc.J:
			poss.append(PcR.J1)
			poss.append(PcR.J2)
			poss.append(PcR.J3)
			poss.append(PcR.J4)
		elif pc is Pc.L:
			poss.append(PcR.L1)
			poss.append(PcR.L2)
			poss.append(PcR.L3)
			poss.append(PcR.L4)
		elif pc is Pc.S:
			poss.append(PcR.S1)
			poss.append(PcR.S2)
		elif pc is Pc.Z:
			poss.append(PcR.Z1)
			poss.append(PcR.Z2)

		return self.simulate_2(poss)

	def simulate_2(self, poss):
		value = [0, 0, 1000]
		for pc in poss:
			spawn = copy.deepcopy(self.playArray)
			self.spawn_w_rot(pc, spawn)
			while not self.move_left(spawn):
				continue
			i=0
			while True:
				arr = copy.deepcopy(spawn)

				while not self.fall_logic(arr):
					continue

				hl, htmp, diff, rew = self.hole_height(arr)
				x1 = 18; x2 = 11; x3 = 0
				if diff > 3:
					x3 = 18
				calc = x1*hl + x2*htmp + x3*diff + rew
				if calc < value[2]:
					value = [pc, i, calc]
				i+=1
				if self.move_right(spawn):
					break
		return value

	def run(self):
		res = (self.resx, self.resy) #Needs Tweaking
		screen = pygame.display.set_mode(res)
		self.screen = screen
		self.init(screen)
		need_new = True

		while self.state is not State.GAME_END:

			for event in pygame.event.get():
				if (event.type == KEYDOWN): 
					if (event.key == K_BACKSPACE):
						self.state = State.GAME_END	#exits if backspace tapped

			piece = self.piece.give()
			value = self.simulate_1(piece)

			spwn = self.spawn_w_rot(value[0])
			if spwn is True:
				break

			while not self.move_left():
				continue

			for i in range(value[1]):
				self.move_right()

			while not self.fall_logic():
				rem = self.check_last(screen)
				self.draw_grid(screen, rem)
				self.oldArray = copy.deepcopy(self.playArray)
				pygame.display.flip()
				time.sleep(0.03)

			"""
			move = None

			#For exiting the game; input parameters go here
			for event in pygame.event.get():
				if (event.type == KEYDOWN): 
					if (event.key == K_BACKSPACE):
						self.state = State.GAME_END	#exits if backspace tapped
					if (event.key == K_LEFT):
						self.move_left()
						move = Move.Left
					if (event.key == K_RIGHT):
						self.move_right()
						move = Move.Right
					#Hard Dropping
					if (event.key == K_DOWN):
						stop = False
						while not stop:
							stop = self.fall_logic()
						time_elapsed_since_last_action = timePerFall
			

			if(time_elapsed_since_last_action > timePerFall):
				need_new = self.fall_logic()
				if need_new == True:
					if self.state is State.GAME_START:
						self.state = State.GAME_CONT
					else:
						self.oldArray = copy.deepcopy(self.playArray)
					fin = self.spawn(screen)
					if fin is True:
						self.state = State.GAME_END
						continue
			"""
			"""
				if need_new == True:
					x = random.randrange(0,self.wd,1)
					if self.state is State.GAME_START:
						self.state = State.GAME_CONT
					else:
						self.oldArray = copy.deepcopy(self.playArray)
					self.playArray[0,x] = 2
			"""