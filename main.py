import time

import pygame
from player import player
pygame.init()

winwidth = 1000
winheight = 700
window = pygame.display.set_mode((winwidth,winheight))
pygame.display.set_caption("Hello World")
run = True
gameclock = pygame.time.Clock()
def redraw():
    window.fill((135,206,235))
    mainchar.move(keys,window)
    pygame.display.update()
mainchar = player(500,350,100,100)
while run:
    gameclock.tick(60) # fps controller
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
  
    redraw()
    
pygame.quit()