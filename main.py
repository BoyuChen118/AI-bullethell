import math,random,time
import pygame
from player import player
from enemies import enemy,enemy2,enemy3
pygame.init()

winwidth = 1000
winheight = 700
window = pygame.display.set_mode((winwidth,winheight))
difficulty = 5
pygame.display.set_caption("Plane Game")
run = True
enemies = []
wavecount = 0  # ten waves in each game
tickcount = 0
gameclock = pygame.time.Clock()
pause = False
background = pygame.image.load("images/nightsky.png")
background = pygame.transform.scale(background, (1000, 700))
Cycle = 0
Over = False  # if the game is over

def determinecycle():  # determine how many cycles to the level
    if difficulty <= 3: # dif 1-3 has 4 cycles
        return 5
    if difficulty <= 5 : # dif 4,5 has 5 cycles
        return 6
    else:
        return 5  # dif 6 (insane mode) has 5 cycles
def checkrands(target,rands): #helper function to spawnenemies()
    if len(rands)!=0:
        for rand in rands:
            if abs(target-rand) <= 70 :  #  if distance between two enemies is within 70 then not ok
                return False
    else:
        return True
    return True
def computewavelength():
    if difficulty <= 3:
        return 4
    elif difficulty == 4:
        return 5
    else:
        return 5

def spawnenemies(Cycle):
    global enemies
    numenemy = (difficulty-3+Cycle) + wavecount
    spawnbias = random.randint(Cycle,numenemy-1)
    numenemy = numenemy - spawnbias
    rands = []
    for i in range(0,numenemy):
        ok = False
        failcounter = 0
        while not ok and failcounter <= 30:  # keep distance between enemies
            x = random.randint(50,950)    # where on the x axis does the plane spawn
            ok = checkrands(x,rands)
            failcounter += 1        # if failed to generate enough distance too many times then go with it
        rands.append(x)
    for rand in rands:
        x = random.randint(0,difficulty-1)     # determine what enemy to generate
        if x == 0:
            e = enemy(rand,0,window)
        elif x == 1:
            e = enemy2(rand,0,window)
        elif x == 2:
            e = enemy3(rand,0,window)
        else:
            e = enemy(rand,0,window)
        enemies.append(e)
        

def checkplayer(player,enemies,Over):
    global pause
    if player.dead:  # player lost
        pause = not pause
        deathtext = bigfont.render('Game Over',1,(255,0,0) )
        window.blit(deathtext, (330,250))

    elif Over and not player.dead and len(enemies) == 0:   # player won
        congrattext = bigfont.render('Congrats You Survived!!',1,(0,255,0) )
        window.blit(congrattext, (130,250))
        congrattext =  font.render('You Score:'+str(mainchar.score),1,(69,123,255) )
        window.blit(congrattext, (330,350))
        # enemies.clear()

def redraw():
    global wavecount
    global tickcount
    global Cycle
    global Over
    window.blit(background,(0,0))
    healthtext = font.render('Health: '+ str(mainchar.health),1,(0,255,0))   # display health
    scoretext = font.render('Score: '+ str(mainchar.score),1,(255,255,0))
    window.blit(healthtext,(800,0))
    window.blit(scoretext,(800,50))
    if Over:   # check if game is over first
        for enemy in enemies:  # check state of all enemies
            if enemy.move(mainchar) and not enemy.dead :
                checkplayer(mainchar,enemies,Over)
                enemy.display() 
            else:
                enemies.pop(enemies.index(enemy))
        checkplayer(mainchar,enemies,Over)
    elif wavecount <= 5+(difficulty-1) and not Over:
        tickcount += 1
        temp = wavecount
        if difficulty <= 5:
            wavecount = tickcount // (300 -50* computewavelength())    # how long each wave lasts
        else:
            wavecount = tickcount // 40

        if wavecount > temp : 
            spawnenemies(Cycle)
        for enemy in enemies:  # check state of all enemies
            if enemy.move(mainchar) and not enemy.dead :
                checkplayer(mainchar,enemies,Over)
                enemy.display() 
            else:
                enemies.pop(enemies.index(enemy))
       
           
    else:
         wavecount = 5
         tickcount = 60 * 5        # once reach wave 8 restart from wave 2
         Cycle += 1
         if Cycle >= determinecycle():
            Over = True
    mainchar.move(keys,window,enemies)
    pygame.display.update()
  
mainchar = player(500,350,100,100)
font = pygame.font.SysFont('comicsans',30,True)
bigfont = pygame.font.SysFont('comicsans',80,True)
while run:
    gameclock.tick(50) # fps controller
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