from pygame.locals import *
import pygame

#Later implement to pieces
class Square(pygame.sprite.Sprite): 
    def __init__(self, par, width = 25): 
        super(Square, self).__init__() 
        self.surf = pygame.Surface((width-1, width-1)) 
        if par == 2:
        	self.surf.fill((0, 200, 255))
        else:
        	self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect() 

class Del_square(pygame.sprite.Sprite): 
    def __init__(self, width = 25): 
        super(Del_square, self).__init__() 
        self.surf = pygame.Surface((width-1, width-1)) 
          
        self.surf.fill((0, 0, 0)) 
        self.rect = self.surf.get_rect() 
