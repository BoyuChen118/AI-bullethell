import math,random,time
import pygame
from player import player
from enemies import enemy,enemy2
pygame.init()

winwidth = 1000
winheight = 700
window = pygame.display.set_mode((winwidth,winheight))
difficulty = 1
pygame.display.set_caption("Hello World")
run = True
enemies = []
wavecount = 0  # ten waves in each game
tickcount = 0
gameclock = pygame.time.Clock()
pause = False
background = pygame.image.load("images/nightsky.png")
background = pygame.transform.scale(background, (1000, 700))



def checkrands(target,rands): #helper function to spawnenemies()
    if len(rands)!=0:
        for rand in rands:
            if abs(target-rand) <= 70 :  #  if distance between two enemies is within 70 then not ok
                return False
    else:
        return True
    return True


def spawnenemies():
    global enemies
    
    numenemy = difficulty * wavecount
    spawnbias = random.randint(0,numenemy-1)
    numenemy = numenemy - spawnbias
    rands = []
    for i in range(0,numenemy):
        ok = False
        failcounter = 0
        while not ok and failcounter <= 30:  # keep distance between enemies
            x = random.randint(100,900)
            ok = checkrands(x,rands)
            failcounter += 1        # if failed to generate enough distance too many times then go with it
        rands.append(x)
    for rand in rands:
        x = random.randint(0,1)     # determine what enemy to generate
        if x == 0:
            e = enemy(rand,0,window)
        else:
            e = enemy2(rand,0,window)
        enemies.append(e)
def checkplayer(player):
    global pause
    if player.dead:
        pause = not pause
def redraw():
    global wavecount
    global tickcount
    window.blit(background,(0,0))
    healthtext = font.render('Health: '+ str(mainchar.health),1,(0,255,0))   # display health
    window.blit(healthtext,(800,0))
    if wavecount <= 12:
        for enemy in enemies:  # check state of all enemies
            if enemy.move(mainchar) and not enemy.dead :
                checkplayer(mainchar)
                enemy.display() 
            else:
                enemies.pop(enemies.index(enemy))
        tickcount += 1
        temp = wavecount
        wavecount = tickcount // 60    # how long each wave lasts
        if wavecount > temp :    
            spawnenemies()
    else:
         wavecount = 5
         tickcount = 60 * 5        # once reach wave 8 restart from wave 2
    mainchar.move(keys,window,enemies)
    pygame.display.update()
  
mainchar = player(500,350,100,100)
font = pygame.font.SysFont('comicsans',30,True)
while run:
    gameclock.tick(60) # fps controller
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        pause = not pause
        time.sleep(0.5)
    if pause:
        continue

    redraw()
pygame.quit()