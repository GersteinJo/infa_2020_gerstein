import pygame
import math as m
from pygame.draw import *

pygame.init()
 
screen = pygame.display.set_mode((300,600))

pygame.display.update()

clock = pygame.time.Clock()
FPS = 30

finished = False

rect(screen, (156,149,120), (0,0,300,300))
ellipse(screen, (220,218,186), (200, 20, 80, 80))

rect(screen, (62,38,36), (10, 150,150,300))
polygon(screen, (10,10,10), [(20,130), (150, 130), (170, 150),(0,150)])
rect(screen, (10,10,10), (10, 150, 10, 150))
rect(screen, (10,10,10), (40, 150, 10, 150))
rect(screen, (10,10,10), (70, 150, 10, 150))
rect(screen, (10,10,10), (100, 150, 10, 150))
rect(screen, (10,10,10), (130, 150, 10, 150))
rect(screen, (115,81,77), (0,300,170,20))
rect(screen, (115,81,77), (0,270,170,10))
rect(screen, (115,81,77), (20, 270, 10, 30))
rect(screen, (115,81,77), (50, 270, 10, 30))
rect(screen, (115,81,77), (80, 270, 10, 30))
rect(screen, (115,81,77), (110, 270, 10, 30))
rect(screen, (115,81,77), (140, 270, 10, 30))

rect(screen, (0,0,0), (20, 350, 30, 30))
rect(screen, (0,0,0), (70, 350, 30, 30))
rect(screen, (220,218,186), (120, 350, 30, 30))



while not finished:
    
    clock.tick(FPS)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
pygame.quit()

'''rect(screen, (255,255,255), (0,0, 400, 400))

ellipse(screen, (255,255,0), (50,50, 300, 300))

ellipse(screen, (255,100,100), (125, 125, 50, 50))
ellipse(screen, (255,100,100), (225, 125, 50, 50))

arc(screen, (0,0,0,155), (75,75, 250,250), m.pi, 2*m.pi)'''