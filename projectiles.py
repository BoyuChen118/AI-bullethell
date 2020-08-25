import pygame

class bullet():  # bullets only move forward
    def __init__(self,xcoord,ycoord,window):
        self.x = xcoord
        self.y = ycoord
        self.velocity = 20
        self.image = pygame.image.load("images/bullet_2_orange.png")
        self.shadow = None
        self.window = window
        self.id = 'b'
    def move(self):
        if self.y - self.velocity >= 0:
            self.y -= self.velocity
            return True
        else:
            return False
class nuke(bullet):
    def __init__(self,xcoord,ycoord,window):
        super().__init__(xcoord,ycoord,window)
        self.velocity = 5
        self.image = pygame.transform.rotate(pygame.image.load("images/rocket_purple.png"),180)
        self.shadow = pygame.image.load("images/bullet_2_purple.png")
        self.id = 'n'
        