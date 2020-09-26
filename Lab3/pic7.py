import pygame
import math as m
from pygame.draw import *
import random

house_col = (62,38,36);
roof_column_col = (10,10,10)
terrace_col = (115,81,77)
wind_on_moon_col = (220,218,186)
wind_off_col = (0,0,0)
clouds_col = (80, 79, 61)
ghost_col = (208, 207, 204)

pygame.init()

def house(x, y, sc, w, h):
    
    #skilleton
    rect(sc, house_col, (x, y, w, h))
    polygon(sc, roof_column_col, [(x-10, y), (x+10, y-20), (x+w-10, y-20), (x+w+10, y)])
    
    #columns and stuff
    col_w = w/11
    for i in range(6):
        rect(sc, roof_column_col, (x+2*col_w*i, y, col_w, h/2))
    rect(sc, terrace_col, (x-10, y + h*2/5, w+20, 10))
    for i in range(5):
        rect(sc, terrace_col, (x+col_w + 2*col_w*i, y + h*2/5+10, col_w, h/10))
    rect(sc, terrace_col, (x-10, y + h/2, w+20, 20))
    
    # windows()
    wind_size = w/3 - 20
    for i in range(3):
        if(random.randint(0, 10)> 6):
            rect(sc, wind_on_moon_col, (x+10 + (20+wind_size)*i, y + 3*h/4, wind_size, wind_size))
        else:
            rect(sc, wind_off_col, (x+10 + (20+wind_size)*i, y + 3*h/4, wind_size, wind_size))

    
def cloud_maker(sc, ymin, ymax, x):
    num = random.randint(3,5)
    for i in range(num):
        x1 = random.randint(0, x)
        y1 = random.randint(ymin, ymax//2)
        w = random.randint(x//3, x//2)
        h = random.randint(ymin//4, w//2)
        ellipse(sc, clouds_col, (x1,y1,w,h))


def ghost_buddy(sc, x_center, y_center):
    r = 30
    ellipse(sc, ghost_col, (x_center - r, y_center - r, 2 * r, 2 * r))
    lowerpoints = []
    lowerpoints.append((x_center - r, y_center))
    for i in range(6):
        ellipse(sc, ghost_col, (x_center - 1.2*r + 10*i, y_center, 21, 2.5*r))
    ellipse(sc, wind_off_col, (x_center - r/3 - 5, y_center-r/2, 10, 20))
    ellipse(sc, wind_off_col, (x_center + r/3 - 5, y_center-r/2, 10, 20))
    ellipse(sc, wind_off_col, (x_center - 7, y_center+r/4, 14, r))
    
        
    
    


screen = pygame.display.set_mode((300,600))

pygame.display.update()

clock = pygame.time.Clock()
FPS = 30

finished = False

rect(screen, (156,149,120), (0,0,300,300))
ellipse(screen, (220,218,186), (200, 20, 80, 80))

cloud_maker(screen, 0, 150, 300)

house(10, 150, screen, 150, 300)

cloud_maker(screen, 0, 150, 300)

ghost_buddy(screen, 200, 400)



while not finished:
    
    clock.tick(FPS)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
pygame.quit()

'''
rect(screen, (255,255,255), (0,0, 400, 400))

ellipse(screen, (255,255,0), (50,50, 300, 300))

ellipse(screen, (255,100,100), (125, 125, 50, 50))
ellipse(screen, (255,100,100), (225, 125, 50, 50))

arc(screen, (0,0,0,155), (75,75, 250,250), m.pi, 2*m.pi)'''