import math,random,time
import pygame
from player import player
from enemies import enemy
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
    rands = []
    for i in range(0,numenemy):
        ok = False
        failcounter = 0
        while not ok and failcounter <= 30:
            x = random.randint(100,900)
            ok = checkrands(x,rands)
            failcounter += 1
        rands.append(x)
    for rand in rands:
        e = enemy(rand,0,window)
        enemies.append(e)

def redraw():
    global wavecount
    global tickcount
    window.fill((135,206,235))
    if wavecount <= 15:
        for enemy in enemies:  # check state of all enemies
            if enemy.move(mainchar) and not enemy.dead :
                enemy.display()
            else:
                enemies.pop(enemies.index(enemy))
        tickcount += 1
        temp = wavecount
        wavecount = tickcount // 120     # how long each wave lasts
        if wavecount > temp :    
            spawnenemies()
    else:
         enemies.clear()
    mainchar.move(keys,window,enemies)
    pygame.display.update()
  
mainchar = player(500,350,100,100)

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