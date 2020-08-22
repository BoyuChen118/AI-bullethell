import pygame,math
from player import player
class enemy():  # standard plane, slow but heavy hitter
    def __init__(self,x,y,window):
        self.health = 18
        self.attack = 50 
        self.x = x
        self.y = y
        self.velocity  = 2
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
        self.scorevalue = 2    # how much score its worth
    def movehitbox(self):
        self.hitboxes[0] = (self.x, self.y+40,110,20)
        self.hitboxes[1] = (self.x+45, self.y+5,18,80)
    def shoot(self,player):
        pass
    def hit(self):
        self.hitted = True
        self.health -= 1
        if self.health <= 0 :
            self.dead = True
    def move(self,player):  # update the enemy's position
        if self.yhitbox[1] + self.velocity <= 700:
            self.y += self.velocity
            self.movehitbox()
            self.detecthit(player)
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
        # self.displayhitbox()
    def displayrotor(self):
        if self.rotorcount <= 4 :
            self.window.blit(self.rotor,(self.x-2,self.y+60))
            self.window.blit(self.rotor,(self.x+60,self.y+60))
        elif self.rotorcount >= 5:
            self.rotorcount = 0 
        self.rotorcount += 1
    def displayhitbox(self):
        pygame.draw.rect(self.window,(255,0,0),self.hitboxes[0],2)
        pygame.draw.rect(self.window,(255,0,0),self.hitboxes[1],2)  # draw hitbox
    def detecthit(self,player):  # detect if player hitbox is inside enemy hitbox
        for hitbox in self.hitboxes:
            box = pygame.Rect(hitbox[0],hitbox[1],hitbox[2],hitbox[3])
            for phitbox in player.hitboxes:
                playerbox = pygame.Rect(phitbox[0],phitbox[1],phitbox[2],phitbox[3])
                if playerbox.colliderect(box): 
                    if player.iframe == 0 :
                        player.hit(self.attack)        # if rects collide minus health from player
                        player.iframe += 1

class enemy2(enemy):  # fast plane with lighter attack
    def __init__(self,x,y,window):
        super().__init__(x,y,window)
        self.image =  pygame.transform.rotate(pygame.image.load("images/Aircraft_10.png"),180)
        self.damaged = pygame.transform.rotate(pygame.image.load("images/Aircraft_10_hit.png"),180)
        self.shadow = pygame.transform.rotate(pygame.image.load("images/Aircraft_10_shadow.png"),180)
        self.velocity = 7
        self.attack = 20
        self.health = 6
        self.hitboxes.append((self.x+5, self.y+30,80,17))
        self.hitboxes.append((self.x+42, self.y+5,10,70))
        self.scorevalue = 1 
    def displayrotor(self):
        pass
    def movehitbox(self):
        self.hitboxes[0]=((self.x+5, self.y+30,80,17))
        self.hitboxes[1]=((self.x+42, self.y+5,10,70))
class enemy3(enemy):  # kamakazi plane with tracking capability
    def __init__(self,x,y,window):
        super().__init__(x,y,window)
        self.image =  pygame.transform.rotate(pygame.image.load("images/more/aircraft_2.png"),180)
        self.damaged = pygame.transform.rotate(pygame.image.load("images/more/aircraft_2_hit.png"),180)
        self.shadow = pygame.transform.rotate(pygame.image.load("images/more/aircraft_2_shadow.png"),180)
        self.velocity = 6
        self.attack = 20
        self.health = 1
        self.hitboxes.append((self.x+5, self.y+30,80,17))
        self.hitboxes.append((self.x+42, self.y+5,10,70))
        self.scorevalue = 1 
    def displayrotor(self):
        pass
    def move(self,player):
        if self.yhitbox[1] + self.velocity <= 700:
                                                    # tracking algorithm
            xdifference = self.x - player.xcoord

            ydifference = self.y - player.ycoord
            if ydifference == 0:  # handle divide by zero error
                self.dead
            angle = math.atan(ydifference/xdifference)
            xvel = self.velocity * math.cos(angle)
            yvel = self.velocity * math.sin(angle)
            if xdifference > 0 and ydifference > 0:
                 self.x -= xvel
                 self.y -= yvel
            elif xdifference > 0  and ydifference < 0:
                 self.x -= xvel
                 self.y -= yvel
            
            else:
                 self.y += yvel
                 self.x += xvel
            self.detecthit(player)
            self.movehitbox()
            return True
        else:
            return False
    def movehitbox(self):
        self.hitboxes[0]=((self.x+5, self.y+30,80,17))
        self.hitboxes[1]=((self.x+42, self.y+5,10,70))
    def detecthit(self,player):  # detect if player hitbox is inside enemy hitbox
        for hitbox in self.hitboxes:
            box = pygame.Rect(hitbox[0],hitbox[1],hitbox[2],hitbox[3])
            for phitbox in player.hitboxes:
                playerbox = pygame.Rect(phitbox[0],phitbox[1],phitbox[2],phitbox[3])
                if playerbox.colliderect(box): 
                    if player.iframe == 0 :
                        player.hit(self.attack)        # if rects collide minus health from player
                        self.dead = True
                        player.iframe += 1

    