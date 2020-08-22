import pygame

class bullet():  # bullets only move forward
    def __init__(self,xcoord,ycoord,window):
        self.x = xcoord
        self.y = ycoord
        self.velocity = 20
        self.image = pygame.image.load("images/bullet_2_orange.png")
        self.window = window
    def move(self):
        if self.y - self.velocity >= 0:
            self.y -= self.velocity
            return True
        else:
            return False