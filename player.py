import pygame,time
from projectiles import bullet
class player():
    def __init__(self,xcoord,ycoord,width,height):
        self.xcoord = xcoord
        self.ycoord = ycoord
        self.velocity = 5
        self.height = height
        self.width = width
        self.rotorcount = 0
        self.mainplane = pygame.image.load("images/Aircraft_08.png")
        self.mainplaneshadow = pygame.image.load("images/Aircraft_08_shadow.png")
        self.rotor = pygame.image.load("images/rotor01.png")
        self.bullets = []
        self.bulletdelay = 0
    def move(self,keys,window,enemies):  #move and draw it self and bullet
        winwidth,winheight = window.get_size()
        if keys[pygame.K_w] and self.ycoord >= self.velocity:
         self.ycoord -= self.velocity
        if keys[pygame.K_s] and self.ycoord <= winheight-(self.height+self.velocity):
            self.ycoord += self.velocity
        if keys[pygame.K_a] and self.xcoord >= self.velocity:
            self.xcoord -= self.velocity
        if keys[pygame.K_d] and self.xcoord <= winwidth-(self.width+self.velocity):
            self.xcoord += self.velocity
        if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
             b = bullet(self.xcoord+20,self.ycoord,window)      #old value : 0
             b2 = bullet(self.xcoord+62,self.ycoord,window)  # old value : +82
             if len(self.bullets)<=18 and self.bulletdelay <= 0:  # limits player bullets on screen under 20
                self.bullets.append(b)
                self.bullets.append(b2)
                self.bulletdelay = 5

        for b in self.bullets:
            displaybullet = True
            for e in enemies:
                for box in e.hitboxes:
                    if b.x > box[0] and b.y > box[1] and b.x < box[0]+box[2] and b.y < box[1]+box[3]:
                        e.hit()
                        displaybullet = False
            if not b.move() or not displaybullet:
                self.bullets.pop(self.bullets.index(b))
            if displaybullet:
                window.blit(b.image,(b.x,b.y))
            

        window.blit(self.mainplaneshadow,(self.xcoord-5,self.ycoord-5))
        window.blit(self.mainplane,(self.xcoord,self.ycoord))
        if self.rotorcount <= 4 :
            window.blit(self.rotor,(self.xcoord+5,self.ycoord+13))
            window.blit(self.rotor,(self.xcoord+47,self.ycoord+13))
        elif self.rotorcount >= 5:
            self.rotorcount = 0 
        
        self.rotorcount+=1

        if self.bulletdelay > 0:
            self.bulletdelay-=1
    def removebullet(self, bullet): #remove bullet that touched the enemy
        self.bullets.pop(self.bullets.index(bullet))