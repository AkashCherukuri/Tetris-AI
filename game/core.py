import numpy as np
import pygame
from pygame.locals import *
from .aes import *
import time

class tetris:
	def __init__(self):
		#Parameters for the board size; maybe add a feature to change board size by exec options?
		self.wd = 10
		self.ht = 20
		self.sz = 25  #Size of each indiv block
		self.pad_x = 40; self.pad_y = 40;
		self.playArray = np.zeros((self.ht, self.wd))
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

	def fill(self, x, y, screen):
		s1 = Square(self.sz)
		dr_x = self.pad_x + self.sz*x + 1
		dr_y = self.pad_y + self.sz*y + 1
		screen.blit(s1.surf, (dr_x, dr_y))

	def delt(self, x, y, screen):
		s1 = Del_square(self.sz)
		dr_x = self.pad_x + self.sz*x + 1
		dr_y = self.pad_y + self.sz*y + 1
		screen.blit(s1.surf, (dr_x, dr_y))

	def run(self):
		res = (720, 720)
		screen = pygame.display.set_mode(res)
		self.init(screen)
		Done = False

		"""
		while not Done:
			#For exiting the game; input parameters go here
			for event in pygame.event.get():
				if event.type == KEYDOWN:
					if event.key == K_BACKSPACE:
						Done = True
		"""

		for x in range(self.wd):
			for y in range(self.ht):
				self.fill(x,y,screen)
				pygame.display.flip()
				time.sleep(0.03)

		for x in range(self.wd):
			for y in range(self.ht):
				self.delt(x,y,screen)
				pygame.display.flip()
				time.sleep(0.03)

		