import pygame
from pygame.draw import *

peach = 245, 175, 127
black = 0, 0, 0
white = 255, 255, 255
green = 44, 105, 56
red = 255, 0, 0

pi = 3.14

resolution = width, height = (1024, 640)

FPS = 30


def leaf(sc, x, y, w, h, angle):
    '''
    This draws one leaf.
    It creates a new surface on which it draws a leaf and then rotates it

    Parameters
    ----------
    sc : base surface.
    x, y: upper left corner of the created surface.
    w, h: width and height of the created surface.
    angle : rotation angle (0 degrees) comply with y axis.

    Returns
    -------
    None.

    '''
    surf = pygame.Surface((int(w), h))
    surf.fill(peach)
    ellipse(surf, green, (0, 0, w, h))
    surf.set_colorkey(peach)
    surface2 = pygame.transform.rotate(surf, angle)
    surface2.set_alpha(255)
    sc.blit(surface2, (x, y))
    

def branch(sc, n, x, y, w, h):
    '''
    Draws a branch

    Parameters
    ----------
    sc : base surface.
    n : number of the branch on the tree starting with lower ones, odd numbers left, even right.
    x, y : upper left corner.
    w, h : width and height of the rectangle which ellipse of the branch inscribed in.

    Returns
    -------
    None.

    '''
    # n for number: even number = right branch, odd number = left branch
    start_angle = pi / 4 *( 1 + ( -1 ) ** n)
    stop_angle = pi / 4 *( 3 + ( -1 ) ** n)
    arc(sc, green, (x, y, w, h), start_angle, stop_angle, 3)
    
    
def leafs(sc, n, x_center, y_center, a, b, interval, leaf_w, leaf_h):
    '''
    Draws leafs on the a given branch

    Parameters
    ----------
    sc : base surface.
    n : number of the branch on the tree starting with lower ones, odd numbers left, even right.
    x_center, y_center : center of the ellipse, arc of which is branch.
    a, b : axles of the ellipse.
    interval : delta x between leafs.
    leaf_w, leaf_h : width and height of the leafs.

    Returns
    -------
    None.

    '''
    for i in range(0, 4):
        xp = (-1) ** (n + 1) * interval * i
        yp = -b * (1 - xp ** 2/ a ** 2) ** (1/2) + y_center
        xp += x_center
        angle = 180 + (-1) ** n * 10
        leaf(sc, xp, yp, leaf_w, leaf_h, angle)
         

def bamboo(sc, x, y, w, h):
    '''
    Draws bamboo

    Parameters
    ----------
    sc : base surface.
    x, y : lower left corner of the trunk.
    w, h : width and height of the trunk.

    Returns
    -------
    None.

    '''
    h_seg = h / 4
    polygon(sc, green, [[x, y - h_seg], [x + w, y - h_seg], [x + w, y], [x, y]])     #
    polygon(sc, green, [[x, int(y - 1.1 * h_seg)], [x, int(y - 1.975 * h_seg)],      #
                        [x + w, int(y - 1.975 * h_seg)], [x + w, y - 1.1 * h_seg]])  #
    polygon(sc, green, [[int(x + w / 2), int(y - 2 * h_seg)],                        #
                        [int(x + w), int(y - 2.9 * h_seg)],                          #
                        [int(x + w / 2), int(y - 3 * h_seg)],                        # trunk of our bamboo
                        [int(x), int(y - 2.1 * h_seg)]])                             #
    polygon(sc, green, [[int(x + w), int(y - 3.05 * h_seg)],                         #
                        [int(x + 3 * w / 2), int(y - 3.95 * h_seg)],                 #
                        [int(x + w), int(y - 4.05 * h_seg)],                         #
                        [int(x + w / 2), int(y - 3.15 * h_seg)]])                    #

    leaf_w, leaf_h = w / 3, h / 6
    a = h_seg
    b = 2 * h_seg
    x_br = x - 2 * a
    y_br = y - 2 * h_seg
        
    for i in range(0, 4):
        # branch itself
        x_br += (-1) ** i * (w + 2 * a)
        y_br -= h_seg / 2
        b_cur = b / (1 + i//2)
        branch(sc, i, x_br, y_br, 2 * a, 2 * b_cur)
        #leafs
        x_leaf_beg = x_br + (1 + (-1) ** (i+1)) * a
        x_leaf_end = x_leaf_beg + a
        leafs(sc, i, x_br + a, y_br + b_cur, a, b_cur, a // 4, leaf_w, leaf_h)
        

def body(sc, x, y, w, h):
    '''
    Draws body of a panda

    Parameters
    ----------
    sc : base surface.
    x, y : upper left corner of panda's body.
    w, h : width and height of panda's body.

    Returns
    -------
    None.

    '''
    ellipse(sc, white, (x, y, w, h))
    ellipse(sc, black, (x, y, w, h), 2)
    
    
def left_leg(sc, x, y, w, h):
    '''
    Left leg of the three legged panda

    Parameters
    ----------
    sc : base surface.
    x, y : upper left corner of panda's body.
    w, h : width and height of panda's body.

    Returns
    -------
    None.

    '''
    polygon(sc, black, [[x, y],
                        [x + int(0.1 * w), y],
                        [x + int(0.15 * w), y + int(1.2 * h)],
                        [x + int(0.05 * w), y + int(1.3 * h)],
                        [x - int(0.05 * w), y + int(1.1 * h)]])
    circle(sc, black, (x + int(0.05 * w), y + int(1.2 * h)), int(h / 5))
    
    
def middle_leg(sc, x, y, w, h):
    '''
    Middle leg of the three legged panda

    Parameters
    ----------
    sc : base surface.
    x, y : upper left corner of panda's body.
    w, h : width and height of panda's body.

    Returns
    -------
    None.

    '''
    ellipse(sc, black, (x + int(0.25 * w), y + int(1.25 * h), int(0.3 * w), int(0.3 * h)))
    ellipse(sc, black, (x + int(0.28 * w), y + int(1.28 * h), int(0.25 * w), int(0.3 * h)))
    ellipse(sc, black, (x + int(0.20 * w), y + int(1.30 * h), int(0.3 * w), int(0.30 * h)))

    polygon(sc, black, [[x + int(0.35 * w), y],
                        [x + int(0.5 * w), y],
                        [x + int(0.5 * w), y + h],
                        [x + int(0.35 * w), y + h]])
    polygon(sc, black, [[x + int(0.3 * w), y + int(1.5 * h)],
                        [x + int(0.55 * w), y + int(1.4 * h)],
                        [x + int(0.5 * w), y + h],
                        [x + int(0.35 * w), y + h]])
    
    
def right_leg(sc, x, y, w, h):
    '''
    Right leg of the three legged panda

    Parameters
    ----------
    sc : base surface.
    x, y : upper left corner of panda's body.
    w, h : width and height of panda's body.

    Returns
    -------
    None.

    '''
    ellipse(sc, black, (x + int(0.85 * w), y + int(0.45 * h), int(0.2 * w), int(0.9 * h)))
    ellipse(sc, black, (x + int(0.8 * w), y + h, int(0.2 * w), int(0.4 * h)))
    
    
def head(sc, x, y, w, h):
    '''
    This is a head of a three legged panda

    Parameters
    ----------
    sc : base surface.
    x, y : upper left corner of panda's body.
    w, h : width and height of panda's body.

    Returns
    -------
    None.

    '''
    circle(sc, black, (x, y - int(0.1 * h)), int(0.2 * h))                      # ear 1

    circle(sc, white, (x + int(0.2 * w), y + int(0.3 * h)), int(0.55 * h))      # head
    circle(sc, black, (x + int(0.2 * w), y + int(0.3 * h)), int(0.55 * h), 2)   

    circle(sc, black, (x + int(0.3 * w), y - int(0.1 * h)), int(0.2 * h))       # ear 2

    circle(sc, black, (x, y + int(0.3 * h)), int(0.1 * h))                      # left eye
    circle(sc, black, (x + int(0.15 * w), y + int(0.3 * h)), int(0.1 * h))      # right eye

    circle(sc, black, (x + int(0.04 * w), y + int(0.6 * h)), int(0.07 * h))     # nose

def panda(sc, x, y, w, h):
    '''
    This is a three legged panda

    Parameters
    ----------
    sc : base surface.
    x, y : upper left corner of panda's body.
    w, h : width and height of panda's body.

    Returns
    -------
    None.

    '''
    body(sc, x, y, w, h)
    left_leg(sc, x, y, w, h)
    middle_leg(sc, x, y, w, h)
    head(sc, x, y, w, h)
    right_leg(sc, x, y, w, h)
    
def scene(sc):
    '''
    draws the scene

    Returns
    -------
    None.

    '''    
    sc.fill(peach)
    bamboo(sc, 200, 500, 30, 400)
    panda(sc, 600, 200, 400, 200)
    panda(sc, 300, 400, 100, 50)


def main():
    '''
    main action is here

    Returns
    -------
    None.

    '''
    pygame.init()

    screen = pygame.display.set_mode(resolution)
    
    scene(screen)
    
    pygame.display.update()
    clock = pygame.time.Clock()
    finished = False
    
    while not finished:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
                
    pygame.quit()

main()


