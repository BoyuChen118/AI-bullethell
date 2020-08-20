import time

import pygame

pygame.init()
winwidth = 1000
winheight = 700
window = pygame.display.set_mode((winwidth,winheight))
pygame.display.set_caption("Hello World")
run = True
gameclock = pygame.time.Clock()
xcoord = 50
ycoord = 50
velocity  = 5
height = 100
width = 100
rotorcount = 0

mainplane = pygame.image.load("images/Aircraft_08.png")
mainplaneshadow = pygame.image.load("images/Aircraft_08_shadow.png")
rotor = pygame.image.load("images/rotor01.png")
def redraw():
    global rotorcount
    window.fill((135,206,235))
    window.blit(mainplaneshadow,(xcoord-5,ycoord-5))
    window.blit(mainplane,(xcoord,ycoord))
    if rotorcount <= 4 :
        window.blit(rotor,(xcoord+5,ycoord+13))
        window.blit(rotor,(xcoord+47,ycoord+13))
        
    elif rotorcount >= 5:
        rotorcount = 0 
    rotorcount+=1
    pygame.display.update()
while run:
    gameclock.tick(60) # fps controller
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w] and ycoord >= velocity:
         ycoord -= velocity
    if keys[pygame.K_s] and ycoord <= winheight-(height+velocity):
        ycoord += velocity
    if keys[pygame.K_a] and xcoord >= velocity:
        xcoord -= velocity
    if keys[pygame.K_d] and xcoord <= winwidth-(width+velocity):
        xcoord += velocity
    redraw()
    
pygame.quit()