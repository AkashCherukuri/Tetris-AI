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
		pygame.init()
	
	def init(self):
		self.playArray = np.zeros((self.ht, self.wd))

	def print_array(self):
		print(self.playArray)

	def run(self):
		res = (720, 720)
		screen = pygame.display.set_mode(res)

		s1 = Square(); _s = E_sq();
		Done = False
		vert = 0;
		while not Done:
			for event in pygame.event.get():
				if event.type == KEYDOWN:
					if event.key == K_BACKSPACE:
						Done = True
			screen.blit(s1.surf, (0,(s1.sz)*(vert)))
			pygame.display.flip()
			vert=vert+1
			screen.blit(_s.surf, (0,(_s.sz)*(vert-1)))
			time.sleep(1)