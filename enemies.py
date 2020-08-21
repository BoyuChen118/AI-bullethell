import pygame
from player import player
class enemy():
    def __init__(self,x,y,window):
        self.health = 10
        self.x = x
        self.y = y
        self.velocity  = 1
        self.image = pygame.image.load("images/Aircraft_02.png")
        self.shadow = pygame.image.load("images/Aircraft_02_shadow.png")
        self.damaged = pygame.transform.rotate(pygame.image.load("images/Aircraft_02_hit.png"),180)
        self.rotor = pygame.transform.rotate(pygame.image.load("images/rotor04.png"),180)
        self.image = pygame.transform.rotate(self.image,180)
        self.shadow = pygame.transform.rotate(self.shadow,180)
        self.window = window
        self.xhitbox = (self.x, self.y+40,110,20) # left,top width,height
        self.yhitbox = (self.x+45, self.y+5,18,80)
        self.hitboxes = []
        self.hitboxes.append(self.xhitbox)
        self.hitboxes.append(self.yhitbox)
        self.hitted = False
        self.dead = False
        self.hitanimation = 0
        self.rotorcount = 0
    def shoot(self):
        pass
    def hit(self):
        self.hitted = True
        self.health -= 1
        if self.health <= 0 :
            self.dead = True
    def move(self,player):  # update the enemy's position
        if self.yhitbox[1] + self.velocity <= 700:
            self.y += self.velocity
            self.hitboxes[0] = (self.x, self.y+self.velocity+40,110,20)
            self.hitboxes[1] = (self.x+45, self.y+self.velocity+5,18,80)
            return True
        else:
            return False
    def display(self):  # display the enemy
        if not self.hitted:
            self.window.blit(self.shadow,(self.x-5,self.y-5))
            self.window.blit(self.image,(self.x,self.y))
        else:
            self.window.blit(self.damaged,(self.x,self.y))
            if self.hitanimation >= 8:
                self.hitted = False
            if self.hitanimation <= 8:
                self.hitanimation += 1    # hitanimation last 8 frames
        self.displayrotor()
    def displayrotor(self):
        if self.rotorcount <= 4 :
            self.window.blit(self.rotor,(self.x-2,self.y+60))
            self.window.blit(self.rotor,(self.x+60,self.y+60))
        elif self.rotorcount >= 5:
            self.rotorcount = 0 
        self.rotorcount += 1
        # pygame.draw.rect(self.window,(255,0,0),self.hitboxes[0],2)
        # pygame.draw.rect(self.window,(255,0,0),self.hitboxes[1],2)  # draw hitbox