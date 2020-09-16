from pygame.locals import *
import pygame

#Later implement to pieces
class Square(pygame.sprite.Sprite): 
    def __init__(self, width = 25): 
        super(Square, self).__init__() 
   		
        self.sz = width
        self.surf = pygame.Surface((width, width)) 
          
        self.surf.fill((0, 200, 255)) 
        self.rect = self.surf.get_rect() 

class E_sq(pygame.sprite.Sprite): 
    def __init__(self, width = 25): 
        super(E_sq, self).__init__() 
   		
        self.sz = width
        self.surf = pygame.Surface((width, width)) 
          
        self.surf.fill((0, 0, 0)) 
        self.rect = self.surf.get_rect() 