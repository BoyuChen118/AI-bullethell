import math,random,time
import neat
import os
import pygame
from player import player
from enemies import enemy,enemy2,enemy3

pygame.init()

winwidth = 1000
winheight = 700
window = pygame.display.set_mode((winwidth,winheight))
difficulty = 3
pygame.display.set_caption("Plane Game")
run = True
training = True
enemies = []
wavecount = 0  # ten waves in each game
tickcount = 0
gameclock = pygame.time.Clock()
pause = False
background = pygame.image.load("images/nightsky.png")
background = pygame.transform.scale(background, (1000, 700))
Cycle = 0
Over = False  # if the game is over
trainingmode = True # enter training mode (train neural network to play the game)
oldmove = 0   # avoid AI doing the same moves
oldmove2 = 0
showhitbox = False  # show enemy hitboxes (for debugging only)
f = pygame.font.SysFont('comicsans',30,True)
bigfont = pygame.font.SysFont('comicsans',80,True)
players = []
networks = []
genes = []
gennum = 0
def determinecycle():  # determine how many cycles to the level
    if difficulty <= 3: # dif 1-3 has 5 cycles
        return 16
    if difficulty <= 5 : # dif 4,5 has 6 cycles
        return 17
    else:
        return 14  # dif 6 (insane mode) has 5 cycles
def checkrands(target,rands): #helper function to spawnenemies()
    if len(rands)!=0:
        for rand in rands:
            if abs(target-rand) <= 70 :  #  if distance between two enemies is within 70 then not ok
                return False
    else:
        return True
    return True
def computewavelength():
    if difficulty <= 2:
        return 4
    else:
        return 5

def spawnenemies(Cycle):
    global enemies
    numenemy = (difficulty-3+(Cycle//2)) + wavecount
    if numenemy <= 0 :  # numenemy can't be 0
        numenemy = 1
    spawnbias = random.randint(Cycle//2,numenemy-1)
    numenemy = numenemy - spawnbias
    rands = []
    anticamp = []  # spawn enemies discourage camping
    for i in range(0,numenemy):
        ok = False
        failcounter = 0
        while not ok and failcounter <= 30:  # keep distance between enemies
            x = random.randint(50,950)    # where on the x axis does the plane spawn
            ok = checkrands(x,rands)
            failcounter += 1        # if failed to generate enough distance too many times then go with it
        rands.append(x)
    if difficulty >= 2 and trainingmode:
        anticamp.append(70)
        anticamp.append(817)
        for a in anticamp:
            e = enemy2(a,0,window)
            enemies.append(e)
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
    global training
    global networks
    global genes
    if player.dead and len(players)>0:
        genes.pop(players.index(player))
        networks.pop(players.index(player))   # remove the gene and network once its host dies
        players.pop(players.index(player))
        if len(players)==0 and trainingmode: 
            training = False    # end generation
    elif player.dead and len(players)==1 and not trainingmode:  
        pause = not pause
        deathtext = bigfont.render('Game Over',1,(255,0,0) )
        window.blit(deathtext, (330,250))


  
    if Over and not player.dead and len(enemies) == 0:   # player won
        if trainingmode:
            training = False
            return 
        congrattext = bigfont.render('Congrats You Survived!!',1,(0,255,0) )
        window.blit(congrattext, (130,250))
        congrattext =  f.render('You Score:'+str(player.score),1,(69,123,255) )
        window.blit(congrattext, (330,350))
        # enemies.clear()

def observe(player): # observe the player's surroundings and find closest dangers
    enemylist = [] # temp copy of list of enemies
    for e in enemies:
        enemylist.append(e)
    retlist = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    counter = 2
    for i in range (0,4):
        dislist = []
        for e in enemylist:
            xdis = abs(e.x-player.xcoord)
            ydis = abs(e.y-player.ycoord)
            dis = math.sqrt(xdis**2+ydis**2)
            dislist.append(dis) 
        if len(dislist)!=0:     
            mindis = min(dislist)   
        else:       
            return retlist
        index = dislist.index(mindis)                       
        retlist[counter] = enemylist[index].hitboxes[0][0]           #append closest enemy's hitbox attributes to list
        counter += 1
        retlist[counter] = enemylist[index].hitboxes[0][2]  
        counter += 1
        retlist[counter] = enemylist[index].y
        counter += 1
        retlist[counter] = enemylist[index].id
        counter += 1
        enemylist.pop(index)
    retlist[0] = player.hitboxes[0][0]
    retlist[1] = player.hitboxes[0][2]
    retlist[2] = player.hitboxes[0][1]
    return retlist
        
def redraw(keys):
    global wavecount
    global tickcount
    global Cycle
    global Over
    global genes
    global run
    global oldmove
    global oldmove2
    window.blit(background,(0,0))
    if len(players)== 1 and not trainingmode:  # single player mode
        healthtext = f.render('Health: '+ str(players[0].health),1,(0,255,0))   # display health
        scoretext = f.render('Score: '+ str(players[0].score),1,(255,255,0))
        window.blit(healthtext,(800,0))
        window.blit(scoretext,(800,50))
    if trainingmode:
        healthtext = f.render('Generation: '+ str(gennum),1,(255,255,255))   # display health
        scoretext = f.render('Population: '+ str(len(players)),1,(255,255,255))
        window.blit(healthtext,(800,0))
        window.blit(scoretext,(800,50))
    if Over:   # check if game is over first
        for enemy in enemies:  # check state of all enemies
                if showhitbox:
                    enemy.showhitbox = True
                if enemy.move(players) and not enemy.dead :
                    for p in players:
                        checkplayer(p,enemies,Over)
                    enemy.display() 
                else:
                    enemies.pop(enemies.index(enemy))
        for p in players:   # check players again after all enemies moved out of frame
              checkplayer(p,enemies,Over)
    elif wavecount <= 5+(difficulty-1) and not Over:
        tickcount += 1
        temp = wavecount
        if difficulty <= 5:
            wavecount = tickcount // (300 -50* computewavelength())    # how long each wave lasts
        else:
            wavecount = tickcount // 40

        if wavecount > temp :  # spawn enemies at start of new wave
            spawnenemies(Cycle)
        for enemy in enemies:  # check state of all enemies
                if showhitbox:
                    enemy.showhitbox = True
                if enemy.move(players) and not enemy.dead :
                    for p in players:
                        checkplayer(p,enemies,Over)
                    enemy.display() 
                else:
                    enemies.pop(enemies.index(enemy))
       
           
    else:    # cycle transition block
        wavecount = 5
        tickcount = 60 * 5        # once reach wave 8 restart from wave 2
        Cycle += 1
        if Cycle >= determinecycle():
            Over = True

    if len(players) == 0 and trainingmode:
        training = False
    for index,p in enumerate(players):  # update player(s) position(s)
        if not trainingmode:
            p.move(keys,window,enemies)
        else:
            genes[index].fitness += 0.01
            genes[index].fitness += p.score//50
            if p.xcoord < 50:
                genes[index].fitness -= 0.3 # avoid camping
            observation  = observe(p)
            output = networks[index].activate(observation)
            for value,o in enumerate(output):
                if o > 0.5:
                    p.action(value,window)
            if p.xcoord != oldmove or p.ycoord != oldmove2:
                genes[index].fitness += 0.2
            oldmove = p.xcoord
            oldmove2 = p.ycoord
            p.fire(window)
            p.check(window,enemies)
    pygame.display.update()


def eval_genomes(genomes,config):
    #initialize everything everytime new generation gets run
    global pause
    global networks
    global genes
    global players
    global Cycle
    global wavecount
    global tickcount
    global enemies
    global oldmoves
    global gennum
    global training,run
    oldmoves = 0
    players = []
    networks = []
    genes = []
    enemies = []

    Cycle = 0
    tickcount = 0
    wavecount = 0
    gennum += 1
    training = True

    for _,genome in genomes:  
        genome.fitness = 0 # initialize fitness to be 0
        network = neat.nn.FeedForwardNetwork.create(genome, config)
        p = player(230,400,100,100)  # x,y,width,height
        players.append(p)
        networks.append(network)
        genes.append(genome)

    for p in players:
        p.health = 1
    while training and len(players) > 0 and run:
        gameclock.tick(50) # fps controller
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                training = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            run = False
        if pause:
            continue

        redraw(keys)




def train(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run for up to 300 generations.
    winner = p.run(eval_genomes, 30)

def main():
    global run
    global pause
    p = player(500,600,100,100)
    players.append(p)
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

        redraw(keys)
    pygame.quit()

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    if trainingmode:
        train(config_path)
    else:
        main()