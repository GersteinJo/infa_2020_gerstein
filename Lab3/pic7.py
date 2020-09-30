import pygame
import math as m
from pygame.draw import *
import math as m
import random

house_col = (35, 22, 22)#(69,44,41);
roof_column_col = (10,10,10)
terrace_col = (95,90,75) #(115,81,77)
wind_on_moon_col = (220,218,186)
wind_off_col = (0,0,0)
clouds_col = (80, 79, 61,100)
new_clouds_col = (186,176,167,100)
ghost_col = (208, 207, 204, 10)
pipe_col = (69, 69, 69)
sky_col= (156,149,120)

field_size = field_size_x, field_size_y = 600, 600

grnd_lvl = 300

pygame.init()

screen = pygame.display.set_mode(field_size)
surface = pygame.display.set_mode((600,600), pygame.SRCALPHA, 32)
screen.blit(surface, (0,0))


def moon(sc, x, y, d):
    '''
    Parameters
    ----------
    sc : surface.
    x : x coordinate of upper left corner.
    y : y coordinate of upper left corner.
    d : diameter

    Returns
    -------
    None.
    '''
    ellipse(screen, wind_on_moon_col, (x, y, d, d))
    
    
def pipes(sc, x_roof, y_roof, w_roof, h_house):
    '''
    Parameters
    ----------
    sc : surface.
    x_roof, y_roof: left upper corner.
    w_roof : width of the higher part of the roof.
    h_house : height of the house.

    Returns
    -------
    None.
    '''
    n = random.randint(1, 6)
    interval_len = w_roof / n
    
    for i in range(n):
        h_pipe = (m.fabs(random.random() - 0.5) + 0.5) * h_house / 10
        w_pipe = (.2 + 0.25 * random.random()) * interval_len
        da_pipe(sc, x_roof + i * interval_len, interval_len, y_roof, w_pipe, h_pipe)


def da_pipe(sc, x_begin_space, interval_len, y_roof, w, h):
    '''
    
    Parameters
    ----------
    sc : surface.
    x_begin_space: the first point of an interval to put the column
    interval_len: length of an interval
    y_roof: upper part.
    w: width of a pipe

    Returns
    -------
    None.

    '''
    x = x_begin_space + random.random() * (interval_len - w)
    rect(sc, pipe_col, (x, y_roof - h, w, h+1))
    
def columns(sc, x_house, y_house, w_house, h_house):
    '''
    Parameters
    ----------
    sc : surface.
    x_house, y_house: left upper corner.
    w_house : width of the house.
    h_house : height of the house.

    Returns
    -------
    None.
    '''
    n = random.randint(4, 7)
    interval_len = w_house / n
    w_column = (.2 + m.fabs((m.fabs(random.random() - .5) - .25))) * interval_len
    h_column = h_house / 2
    for i in range(n):
        x_column = x_house + i * interval_len + (interval_len - w_column) / 2
        da_column(sc, x_column, y_house, w_column, h_column)
    
    
def da_column(sc, x_column, y_column, w_column, h_column):
    '''
    Parameters
    ----------
    sc : surface.
    x_column, y_column : coordinate of upper left corner.
    w_column : width of a column.
    h_column : height of a column.

    Returns
    -------
    None.

    '''
    rect(sc, roof_column_col, (x_column, y_column, w_column, h_column))
    

def terrace(sc, x_house, y_house, w_house, h_house):
    '''
    Parameters
    ----------
    sc : surface.
    x_house, y_house: left upper corner.
    w_house : width of the house.
    h_house : height of the house.

    Returns
    -------
    None.
    '''
    rect(sc, terrace_col, (x_house - w_house / 15, y_house + h_house / 2, w_house * 17 / 15, h_house / 15))
    n = random.randint(4, 9)
    interval_len = 17 / 15 * w_house / n
    w_barrel = (.1 + m.fabs((m.fabs(random.random() - .5) - .25))) * interval_len
    h_barrel = h_house / 5
    for i in range(n):
        x_barrel = x_house - w_house / 15 + i * interval_len + (interval_len - w_barrel) / 2
        da_barrel(sc, x_barrel, y_house + .3 * h_house, w_barrel, h_barrel)
    rect(sc, terrace_col, (x_house - w_house / 15, y_house + .3 * h_house, w_house * 17 / 15, w_barrel))
    

def da_barrel(sc, x_barrel, y_barrel, w_barrel, h_barrel):
    '''
    Parameters
    ----------
    sc : surface.
    x_barrel, y_barrel : coordinate of upper left corner.
    w_barrel : width of a barrel.
    h_barrel : height of a barrel.

    Returns
    -------
    None.

    '''
    rect(sc, terrace_col,(x_barrel, y_barrel, w_barrel, h_barrel))


def windows(sc, x_house, y_house, w_house, h_house):
    '''
    Parameters
    ----------
    sc : surface.
    x_house, y_house: left upper corner.
    w_house : width of the house.
    h_house : height of the house.

    Returns
    -------
    None.
    '''
    n = random.randint(2, 5)
    interval_len = w_house / n
    window_size = .8 * interval_len
    for i in range(n):
        x_window = x_house + (i + .1) * interval_len
        da_window(sc, x_window, y_house + 3 / 4 * h_house - .5 * window_size, window_size)


def da_window(sc, x_window, y_window, window_size):
    '''
    Parameters
    ----------
    sc : surface.
    x_window, y_window: left upper corner.
    window_size : side of a square

    Returns
    -------
    None.
    '''
    if random.random() > 0.65:
        rect(sc, wind_on_moon_col, (x_window, y_window, window_size, window_size))
    else:
        rect(sc, wind_off_col, (x_window, y_window, window_size, window_size))


def house(sc, x, y, w, h, red, green, blue):
    '''
    

    Parameters
    ----------
    sc : surface.
    x, y : higher upper corner of the skilleton.
    w, h : width and height of the house.
    red, green, blue : parameters to make further buildings darker basic colors.

    Returns
    -------
    None.

    '''
    house_color = red, green, blue
    
    #skilleton
    rect(sc, house_color, (x, y, w, h))
    polygon(sc, roof_column_col, [(x-w/15, y), (x+w/15, y-h/15), (x+14*w/15, y-h/15), (x+16*w/15, y)])
    
    #decorations
    pipes(sc, x+w/15, y-h/15, w*13/15, h)
    columns(screen, x, y, w, h)
    terrace(screen, x, y, w, h)
    windows(screen, x, y, w, h)
    
        
def cloud_maker(sc, ymin, ymax, x, color):
    '''
    Parameters
    ----------
    sc : surface.
    ymin, ymax : max and min height for clouds.
    x : max remoteness axis X.
    color : color of the clouds.

    Returns
    -------
    None.

    '''
    num = random.randint(3,5)
    for i in range(num):
        x1 = random.randint(0, x)
        y1 = random.randint(ymin, ymax//2)
        w = random.randint(x//3, x//2)
        h = random.randint(ymin//10, w//5)
        ellipse(sc, color, (x1,y1,2*w,h))


def ghost_buddy(sc, x_center, y_center, r):
    '''
    Parameters
    ----------
    sc : surface.
    x_center, y_center : center of the ghost's head.
    r : radius of the ghost's head.

    Returns
    -------
    None.

    '''
    ellipse(sc, ghost_col, (x_center - r, y_center - r, 2 * r, 2 * r))
    lowerpoints = []
    lowerpoints.append((x_center - r, y_center))
    lowerpoints.append((x_center - 1.2 * r, y_center + 2.5 * r))
    lowerpoints.append((x_center - r, y_center + 2.9 * r))
    lowerpoints.append((x_center, y_center + 3 * r))
    lowerpoints.append((x_center + r, y_center + 2.9 * r))
    lowerpoints.append((x_center + 1.2 * r, y_center + 2.5 * r))
    lowerpoints.append((x_center + r, y_center))
    polygon(sc, ghost_col, lowerpoints)
    ellipse(sc, wind_off_col, (x_center - r/3 - r/6, y_center-r/2, r/3, r))
    ellipse(sc, wind_off_col, (x_center + r/3 - r/6, y_center-r/2, r/3, r))
    ellipse(sc, wind_off_col, (x_center - r/4, y_center+r/4, r/2, r))
    

pygame.display.update()

clock = pygame.time.Clock()
FPS = 30

finished = False

#sky
rect(screen, (156,149,120), (0,0,field_size_x,field_size_y - grnd_lvl))
moon(screen, 200, 20, 80)
cloud_maker(surface, 0, 150, field_size_x, clouds_col)

houses_info = []

house_x = random.randint(10, field_size_x - 100)
house_y = random.randint(100, (field_size_y - grnd_lvl) * 2 // 3)
house_h = random.randint(field_size_y - grnd_lvl - house_y, (field_size_y - grnd_lvl - house_y) * 2)
house_w = random.randint(house_h // 2, house_h * 2 // 3)
houses_info.append([house_x, house_y, house_w, house_h])

while len(houses_info) < 3:
    house_x = random.randint(10, field_size_x - 100)
    house_y = random.randint(150, (field_size_y - grnd_lvl) * 2 // 3)
    house_h = (field_size_y - grnd_lvl - house_y) * 2
    house_w = random.randint(house_h // 2, house_h * 2 // 3)
    good_place = True
    
    for hi in houses_info:
        if (hi[0] - house_x) ** 2 < field_size_x ** 2 / 25 and (hi[1] - house_y) ** 2 < field_size_y ** 2 / 9:
            good_place = False
    
    if good_place:
        if house_h > houses_info[- 1][3]:
            houses_info.append([house_x, house_y, house_w, house_h])
        elif house_h < houses_info[0][3]:
            houses_info.insert(0, [house_x, house_y, house_w, house_h])

for hi in houses_info:
    r, g, b = house_col
    r, g, b = r + 20, g + 15, b + 15
    house_col = r, g, b
    house(screen, hi[0], hi[1], hi[2], hi[3], r, g, b)

cloud_maker(surface, 0, 150, field_size_x, new_clouds_col)

ghost_info = []

while len(ghost_info) < 3:
    ghost_is_not_on_house = 0

    while (ghost_is_not_on_house == 0):
        not_on_house = []
        ghost_x = random.randint(0, field_size_x)
        for hi in houses_info:
            if ghost_x >= hi[0] and ghost_x <= hi[0] + hi[2]:
                not_on_house.append(0)
            else:
                    not_on_house.append(1)
            
            ghost_is_not_on_house = 1

        for noh in not_on_house:
            ghost_is_not_on_house *= noh

    ghost_r = random.randint(20,30)        
    ghost_y = random.randint(field_size_y - grnd_lvl, field_size_y - 3*ghost_r)

    ghost_info.append([ghost_x, ghost_y, ghost_r])

for ghost in ghost_info:
    ghost_buddy(screen, ghost[0], ghost[1], ghost[2])
    

cloud_maker(surface, 200, 600, field_size_x, new_clouds_col)

screen.blit(surface, (0,0))

while not finished:
    
    clock.tick(FPS)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
pygame.quit()
