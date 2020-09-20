import numpy as np
import pygame
import time, random, copy
import itertools
from pygame.locals import *
from .aes import *
from .states import State, Gen_P, Pc, Move
from .utils import sh_d_one

colorRGBGrey = (169,169,169)

class tetris:
	def __init__(self):
		#Parameters for the board size; maybe add a feature to change board size by exec options?
		self.wd = 10
		self.ht = 20
		self.sz = 25  #Size of each indiv block
		self.pad_x = 40; self.pad_y = 40;
		self.resx = 720; self.resy = 720;
		self.playArray = np.zeros((self.ht, self.wd))		#0-Empty, (1)-Placed, 2-Moving
		self.oldArray = np.zeros((self.ht, self.wd))		#For erasing earlier grid
		self.state = State.GAME_START
		self.piece = Gen_P()
		pygame.init()
	
	#Draw borders and basic UI borders
	#TODO: ADD SCORES
	def init(self, screen):
		scrn = Del_square(max(self.resx, self.resy))
		for x in range(self.wd+1):
			inc = x*self.sz
			pygame.draw.line(screen, colorRGBGrey, (self.pad_x+inc, self.pad_y), (self.pad_x+inc, self.pad_y+self.ht*self.sz))
		for y in range(self.ht+1):
			inc=y*self.sz
			pygame.draw.line(screen, colorRGBGrey, (self.pad_x, self.pad_y+inc), (self.pad_x+self.sz*self.wd, self.pad_y+inc))
		pygame.display.flip()

	def fill(self, x, y, screen, par):
		s1 = Square(par,self.sz)
		dr_x = self.pad_x + self.sz*x + 1
		dr_y = self.pad_y + self.sz*y + 1
		screen.blit(s1.surf, (dr_x, dr_y))

	def delt(self, x, y, screen):
		s1 = Del_square(self.sz)
		dr_x = self.pad_x + self.sz*x + 1
		dr_y = self.pad_y + self.sz*y + 1
		screen.blit(s1.surf, (dr_x, dr_y))

	def draw_grid(self, screen, rem):
		old_grid = np.where(self.oldArray == 2)
		y_idx = old_grid[0]; x_idx = old_grid[1]
		for (x,y) in zip(x_idx,y_idx):
			self.delt(x,y,screen)

		if rem > 0:
			old_grid = np.where(self.oldArray == 1)
			y_idx = old_grid[0]; x_idx = old_grid[1]
			for (x,y) in zip(x_idx,y_idx):
				self.delt(x,y,screen)
		
		new_grid = np.where(self.playArray == 1)
		y_idx = new_grid[0]; x_idx = new_grid[1]
		for (x,y) in zip(x_idx,y_idx):
			self.fill(x,y,screen,1)

		new_grid = np.where(self.playArray == 2)
		y_idx = new_grid[0]; x_idx = new_grid[1]
		for (x,y) in zip(x_idx,y_idx):
			self.fill(x,y,screen,2)

	#return False if successful, else return True to indicate GameOver
	def spawn(self, screen):
		new = self.piece.give()
		#Python has no switch statement lul; use dict-mapping maybe?
		
		if new is Pc.I:
			for i in range((self.wd//2)-2, (self.wd//2)+2):
				if self.playArray[0,i] == 1:
					return True
			for i in range((self.wd//2)-2, (self.wd//2)+2):
				self.playArray[0,i] = 2

		elif new is Pc.O:
			for i in range((self.wd//2)-1, (self.wd//2)+1):
				if self.playArray[1,i] == 1:
					return True
			for i in range((self.wd//2)-1, (self.wd//2)+1):
				self.playArray[0,i] = 2
				self.playArray[1,i] = 2

		elif new is Pc.T or new is Pc.J or new is Pc.L:
			for i in range((self.wd//2)-1, (self.wd//2)+2):
				if self.playArray[1,i] == 1:
					return True
			for i in range((self.wd//2)-1, (self.wd//2)+2):
				self.playArray[1,i] = 2
			if new is Pc.J:
				self.playArray[0, (self.wd//2)-1] = 2
			elif new is Pc.T:
				self.playArray[0, (self.wd//2)] = 2
			else:
				self.playArray[0, (self.wd//2)+1] = 2
	
		elif new is Pc.S:
			for i in range((self.wd//2)-1, (self.wd//2)+1):
				if self.playArray[1,i] == 1:
					return True
			self.playArray[1, (self.wd//2)-1] = 2
			self.playArray[1, (self.wd//2)] = 2
			self.playArray[0, (self.wd//2)] = 2
			self.playArray[0, (self.wd//2)+1] = 2

		elif new is Pc.Z:
			for i in range((self.wd//2), (self.wd//2)+2):
				if self.playArray[1,i] == 1:
					return True
			self.playArray[1, (self.wd//2)+1] = 2
			self.playArray[1, (self.wd//2)] = 2
			self.playArray[0, (self.wd//2)] = 2
			self.playArray[0, (self.wd//2)-1] = 2			


		return False
	
	#Remove the last filled line, return number of lines that were filled
	#TODO: Checks only last row
	def check_last(self, screen, cnt):
		fill = True
		for x in range(self.wd):
			if self.playArray[self.ht-1, x] != 1:
				fill = False
				break
		if fill:
			sh_d_one(self.playArray, self.ht, self.wd)
			return self.check_last(screen, cnt+1)
		return cnt

	#At the max, we'll have only one moving piece; bool fn
	def fall_logic(self):
		fall_block = np.where(self.playArray == 2)
		y_idx = fall_block[0][::-1]; x_idx = fall_block[1][::-1]
		if (y_idx.size == 0 and x_idx.size == 0):
			return True
		check = False
		for (x,y) in zip(x_idx,y_idx):
			if y == self.ht-1:	
				check = True
			elif self.playArray[y+1,x] == 1:
				check = True

		if check is True:
			for (x,y) in zip(x_idx,y_idx):
				self.playArray[y,x] = 1
			return True

		for (x,y) in zip(x_idx,y_idx):
			self.playArray[y,x] = 0
		for (x,y) in zip(x_idx,y_idx):
			self.playArray[y+1,x] = 2
		return False

	def move_left(self):
		fall_block = np.where(self.playArray == 2)
		y_idx = fall_block[0][::-1]; x_idx = fall_block[1][::-1]
		if (y_idx.size == 0 and x_idx.size == 0):
			return True
		check = False
		for (x,y) in zip(x_idx,y_idx):
			if (x == 0 or self.playArray[y,x-1] == 1):
				check = True

		if check is True:
			return True

		for (x,y) in zip(x_idx,y_idx):
			self.playArray[y,x] = 0
		for (x,y) in zip(x_idx,y_idx):
			self.playArray[y,x-1] = 2

		return False

	def move_right(self):
		fall_block = np.where(self.playArray == 2)
		y_idx = fall_block[0][::-1]; x_idx = fall_block[1][::-1]
		if (y_idx.size == 0 and x_idx.size == 0):
			return True
		check = False
		for (x,y) in zip(x_idx,y_idx):
			if (x == self.wd-1 or self.playArray[y,x+1] == 1):
				check = True

		if check is True:
			return True

		for (x,y) in zip(x_idx,y_idx):
			self.playArray[y,x] = 0
		for (x,y) in zip(x_idx,y_idx):
			self.playArray[y,x+1] = 2

		return False

	def run(self):

		timePerFall = 350

		res = (self.resx, self.resy) #Needs Tweaking
		screen = pygame.display.set_mode(res)
		self.init(screen)
		need_new = True

		time_elapsed_since_last_action = 0
		clock = pygame.time.Clock()

		while self.state is not State.GAME_END:

			dt = clock.tick()
			time_elapsed_since_last_action += dt

			if self.state is State.GAME_CONT:
				self.oldArray = copy.deepcopy(self.playArray)

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
				if need_new == True:
					x = random.randrange(0,self.wd,1)
					if self.state is State.GAME_START:
						self.state = State.GAME_CONT
					else:
						self.oldArray = copy.deepcopy(self.playArray)
					self.playArray[0,x] = 2
				"""
				time_elapsed_since_last_action = 0
			rem = self.check_last(screen,0)
			self.draw_grid(screen, rem)
			pygame.display.flip()