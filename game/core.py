import numpy as np
import pygame
import time, random, copy
import itertools
from pygame.locals import *
from .aes import *
from .states import State, Gen_P, Pc

class tetris:
	def __init__(self):
		#Parameters for the board size; maybe add a feature to change board size by exec options?
		self.wd = 10
		self.ht = 20
		self.sz = 25  #Size of each indiv block
		self.pad_x = 40; self.pad_y = 40;
		self.playArray = np.zeros((self.ht, self.wd))		#0-Empty, (1)-Placed, 2-Moving
		self.oldArray = np.zeros((self.ht, self.wd))		#For erasing earlier grid
		self.state = State.GAME_START
		self.piece = Gen_P()
		pygame.init()
	
	#Draw borders and basic UI borders, make scalable later
	#TODO: ADD SCORES
	def init(self, screen):
		for x in range(self.wd+1):
			inc = x*self.sz
			pygame.draw.line(screen, (169,169,169), (self.pad_x+inc, self.pad_y), (self.pad_x+inc, self.pad_y+self.ht*self.sz))
		for y in range(self.ht+1):
			inc=y*self.sz
			pygame.draw.line(screen, (169,169,169), (self.pad_x, self.pad_y+inc), (self.pad_x+self.sz*self.wd, self.pad_y+inc))
		pygame.display.flip()

	#At the max, we'll have only one moving piece; bool fn
	#DEBUG TO CHANGE ALL 2 to 1
	def fall_logic(self):
		fall_block = np.where(self.playArray == 2)
		y_idx = fall_block[0][::-1]; x_idx = fall_block[1][::-1]
		check = False
		for (x,y) in zip(x_idx,y_idx):
			if y == self.ht-1:
				self.playArray[y,x] = 1
				check = True
			elif self.playArray[y+1,x] == 1:
				self.playArray[y,x] = 1
				check = True

		if check is True:
			for (x,y) in zip(x_idx,y_idx):
				self.playArray[y,x] = 1
				return True

		for (x,y) in zip(x_idx,y_idx):
			self.playArray[y+1,x] = 2
			self.playArray[y,x] = 0
		return False

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

	def draw_grid(self, screen):
		new_grid = np.where(self.playArray == 2)
		y_idx = new_grid[0]; x_idx = new_grid[1]
		for (x,y) in zip(x_idx,y_idx):
			self.fill(x,y,screen,2)

		new_grid = np.where(self.playArray == 1)
		y_idx = new_grid[0]; x_idx = new_grid[1]
		for (x,y) in zip(x_idx,y_idx):
			self.fill(x,y,screen,1)

		old_grid = np.where(self.oldArray == 2)
		y_idx = old_grid[0]; x_idx = old_grid[1]
		for (x,y) in zip(x_idx,y_idx):
			self.delt(x,y,screen)

	#return False if successful, else return True to indicate GameOver
	def spawn(self, screen):
		new = self.piece.give()
		#Python has no switch statement lul; use dict-mapping maybe?
		
		if True:
			for i in range((self.wd//2)-2, (self.wd//2)+2, 1):
				if self.playArray[0,i] == 1:
					return True
			for i in range((self.wd//2)-2, (self.wd//2)+2, 1):
				self.playArray[0,i] = 2

		"""
		if True:
			for i in range((self.wd//2)-1, (self.wd//2)+1, 1):
				if self.playArray[1,i] == 1:
					return True
			for i in range((self.wd//2)-1, (self.wd//2)+1, 1):
				self.playArray[0,i] = 2
				self.playArray[1,i] = 2
		return False
		"""

	def run(self):
		res = (720, 720) #Needs Tweaking
		screen = pygame.display.set_mode(res)
		self.init(screen)
		need_new = True

		while self.state is not State.GAME_END:
			#For exiting the game; input parameters go here
			for event in pygame.event.get():
				if event.type == KEYDOWN:
					if event.key == K_BACKSPACE:
						self.state = State.GAME_END

			if self.state is State.GAME_CONT:
				self.oldArray = copy.deepcopy(self.playArray)

			if need_new == True:
				if self.state is State.GAME_START:
					self.state = State.GAME_CONT
				else:
					self.oldArray = copy.deepcopy(self.playArray)
				fin = self.spawn(screen)
				if fin is True:
					self.state = State.GAME_END
					continue


			need_new = self.fall_logic()
			self.draw_grid(screen)
			pygame.display.flip()
			time.sleep(0.3)