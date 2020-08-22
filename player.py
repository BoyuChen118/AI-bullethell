import pygame,time
from projectiles import bullet
class player():
    def __init__(self,xcoord,ycoord,width,height):
        self.health = 100
        self.xcoord = xcoord
        self.ycoord = ycoord
        self.velocity = 8
        self.height = height
        self.width = width
        self.rotorcount = 0
        self.mainplane = pygame.image.load("images/Aircraft_08.png")
        self.mainplaneshadow = pygame.image.load("images/Aircraft_08_shadow.png")
        self.damaged = pygame.image.load("images/Aircraft_08_hit.png")
        self.rotor = pygame.image.load("images/rotor01.png")
        self.bullets = []
        self.bulletdelay = 0
        self.hitboxes = []
        self.xhitbox = (self.xcoord,self.ycoord+22,90,20)   # horizontal hitbox
        self.yhitbox = (self.xcoord+40,self.ycoord,10,70)   # vertical hitbox
        self.hitboxes.append(self.xhitbox)
        self.hitboxes.append(self.yhitbox)
        self.iframe = 0
        self.dead = False
        self.score = 0
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
                self.bulletdelay = 5          # adjust shooting speed (lower the faster)
        self.hitboxes[0] = (self.xcoord,self.ycoord+22,90,20)
        self.hitboxes[1] = (self.xcoord+40,self.ycoord,10,70)
        for b in self.bullets:     # bullet detection !
            displaybullet = True
            for e in enemies:
                for box in e.hitboxes:
                    if b.x > box[0] and b.y > box[1] and b.x < box[0]+box[2] and b.y < box[1]+box[3]:
                        e.hit()
                        displaybullet = False
                        if e.dead:    # increment score if scores a kill
                            self.score += e.scorevalue
            if not b.move() or not displaybullet:
                self.bullets.pop(self.bullets.index(b))
            if displaybullet:
                window.blit(b.image,(b.x,b.y))
            

        window.blit(self.mainplaneshadow,(self.xcoord-5,self.ycoord-5))
        window.blit(self.mainplane,(self.xcoord,self.ycoord))
        # pygame.draw.rect(window,(255,0,0),self.hitboxes[0],2)
        # pygame.draw.rect(window,(255,0,0),self.hitboxes[1],2)   # draw hitbox
        if self.rotorcount <= 4 :
            window.blit(self.rotor,(self.xcoord+5,self.ycoord+13))
            window.blit(self.rotor,(self.xcoord+47,self.ycoord+13))
        elif self.rotorcount >= 5:
            self.rotorcount = 0 
        
        self.rotorcount+=1
        
        if self.iframe >= 60:
            self.iframe = 0
        elif self.iframe < 60 and self.iframe > 0 :  # while in iframe
            self.iframe += 1
            if self.iframe % 5  != 0 :  # flashes for 5 frames at a time
                window.blit(self.damaged,(self.xcoord,self.ycoord))

        if self.bulletdelay > 0:
            self.bulletdelay-=1
    def hit(self,dmg):   # subtract dmg from health if hit
        self.health -= dmg 
        if self.health <= 0 :
            self.dead = True