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
	def init(self, screen):
		for x in range(self.wd+1):
			inc = x*self.sz
			pygame.draw.line(screen, (169,169,169), (self.pad_x+inc, self.pad_y), (self.pad_x+inc, self.pad_y+self.ht*self.sz))
		for y in range(self.ht+1):
			inc=y*self.sz
			pygame.draw.line(screen, (169,169,169), (self.pad_x, self.pad_y+inc), (self.pad_x+self.sz*self.wd, self.pad_y+inc))
		pygame.display.flip()

	def print_array(self):
		print(self.playArray)


	def run(self):
		res = (720, 720)
		screen = pygame.display.set_mode(res)
		self.init(screen)
		s1 = Square(self.sz); _s = Del_square(self.sz);
		Done = False
		vert = 0;
		while not Done:
			#For exiting the game
			for event in pygame.event.get():
				if event.type == KEYDOWN:
					if event.key == K_BACKSPACE:
						Done = True
			screen.blit(s1.surf, (self.pad_x+1,self.pad_y+1+(self.sz)*(vert)))
			pygame.display.flip()
			vert=vert+1
			screen.blit(_s.surf, (self.pad_x+1,self.pad_y+1+(self.sz)*(vert-1)))
			time.sleep(1)