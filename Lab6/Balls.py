import pygame
from pygame.draw import *
from random import randint
pygame.init()


RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
mint = (170,255, 234)
falling_cube_color = (199, 200, 226)

FPS = 150
resolution = width, height = 1200, 600

Score = 0
balls = []
cubes = []
screen = pygame.display.set_mode(resolution)
g = 0.05

leaders_table = open('C:/Users/Яна/OneDrive/Documents/Uni/Семестр 1/прога/GitHub/infa_2020_gerstein/Lab6/leaders_table.txt', 'r')
players = []
scores = []

for line in leaders_table:
    a, b = line.split()
    print(a, b)
    players.append(a)
    scores.append(int(b))

leaders_table.close()

txt_x, txt_y = 300, 10
inscription_font = pygame.font.SysFont('Arial Black', 22)
inscription = inscription_font.render("You scored: " + str(Score), 5, mint) # inscription
screen.blit(inscription, (width - txt_x, txt_y)) # where to


def new_ball():
    '''
    This creates a new ball
    
    return None
    '''
    x = randint(100, width - 100)
    y = randint(100, height - 100)
    r = randint(10, 100)
    num_color = randint(0, 5)
    vx = randint(-2, 2)
    vy = randint(-2, 2)
    return(x, y, r, num_color, vx, vy)

def draw_ball(x, y, r, num_color):
    '''
    this drawsa ball
    Parameters
    x, y : center of the ball
    r : radius
    num_color : parameter that defines the color
    return None
    '''
    circle(screen, COLORS[num_color], (x, y), r)
    
def move_ball(x, y, r, vx, vy):
    '''
    this returns new coordinates of ball's center
    Parameters
    x, y : coordinates of the center
    r : radius
    vx : x-velocity
    vy : y-velocity
    return None
    '''
    if x + r > width:
        vx = 0 - vx
        x = width - r
    
    if x - r < 0:
        vx = 0 - vx
        x = r
        
    
    if y + r > height:
        vy = 0 - vy
        y = height - r
    
    if y - r < 0:
        vy = 0 - vy
        y = r

    x, y = x + vx, y + vy
    return(x, y, vx, vy)    

def ball_caught(x_mouse, y_mouse, x_ball, y_ball, r_ball):
    '''
    Checks if the ball's been caught

    Parameters
    ----------
    x_mouse, y_mouse : coordinates of mouse
    x_ball, y_ball : coordinates of the center of the ball
    r_ball : radius of the ball

    Return 
    -------
    caught : bool.

    '''
    R = ((x_ball - x_mouse) ** 2 + (y_ball - y_mouse) ** 2) ** (1/2)
    if(R <= r_ball):
        caught = True
    else:
        caught = False
    return caught

def new_falling_cube():
    '''
    Creates new cube
    Parameters
    a : length of a side of the cube
    xc, yc : coordinates of upper left corner
    vyc : y-velocity

    Returns
    -------
    None.

    '''
    a = randint(50, 70)
    xc = randint(100, width - 100)
    yc = -a
    vyc = 0
    print(xc, yc, a, vyc)
    return(xc, yc, a, vyc)

def draw_falling_cube(xc, yc, a):
    '''
    Draws the cube

    Parameters
    ----------
    xc, yc : current coordinates of upper left corner
    a : length of a side.

    Returns
    -------
    None.

    '''
    rect(screen, falling_cube_color, (xc, yc, a, a))
    
def move_falling_cube(h, v):
    '''
    Changes y coordinate of the cube
    Parameters
    h : y coordinate
    v : y velocity
    '''
    v -= g
    h -= v
    return(h, v)

def cube_caught(x_mouse, y_mouse, x_cube, y_cube, a_cube):
    '''
    Checks if the cube's been caught

    Parameters
    ----------
    x_mouse, y_mouse : coordinates of mouse
    x_cube, y_cube : coordinates of the upper left corner
    a_cube : length of a side

    Return 
    -------
    caught : bool.

    '''
    if abs(x_mouse-x_cube) < a_cube and abs(y_mouse-y_cube) < a_cube:
        return True
    else:
        return False



pygame.display.update()
clock = pygame.time.Clock()
finished = False

x, y, r, num_color, vx, vy = new_ball()
alive = 1
balls.append([x, y, r, num_color, vx, vy, alive])

xc, yc, a, vyc = new_falling_cube()
cubes.append([xc, yc, a, vyc])
draw_falling_cube(xc, yc, a)


while not finished:
    clock.tick(FPS)
    for b in balls:
        b[0], b[1], b[4], b[5] = move_ball(b[0], b[1], b[2], b[4], b[5])
        draw_ball(b[0], b[1], b[2], b[3])
        
    for c in cubes:
        c[1], c[3] = move_falling_cube(c[1], c[3])
        if(c[1] > height):
            cubes.remove(c)
        else:
            draw_falling_cube(c[0], c[1], c[2])
        
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for b in balls:
                x_mouse, y_mouse = event.pos
                caught = ball_caught(x_mouse, y_mouse, b[0], b[1], b[2])
                if caught:
                    Score += 10
                    balls.remove(b)
                    break
            for c in cubes:
                x_mouse, y_mouse = event.pos
                caught = cube_caught(x_mouse, y_mouse, c[0], c[1], c[2])
                if caught:
                    Score += 20
                    cubes.remove(c)
                    break
                
    inscription = inscription_font.render("You scored: " + str(Score), 5, mint) # inscription
    screen.blit(inscription, (width - txt_x, txt_y))

    for b in balls:
        if b[6] == 0:
            balls.remove(b)
            print('removed')
    
    if len(balls) < 10:
        x, y, r, num_color, vx, vy = new_ball()
        alive = 1
        balls.append([x, y, r, num_color, vx, vy, alive])
        
    if len(cubes) < 5:
        xc, yc, a, vyc = new_falling_cube()
        cubes.append([xc, yc, a, vyc])
        
    
    pygame.display.update()
    screen.fill(BLACK)

pygame.display.quit()
print(Score)
for i in range(0, len(players)):
    if(scores[i] < Score):
        scores.insert(i, Score)
        players.insert(i, input('Whats your name? Dont use spaces.\n' ))
        break
        
leaders_table = open('C:/Users/Яна/OneDrive/Documents/Uni/Семестр 1/прога/GitHub/infa_2020_gerstein/Lab6/leaders_table.txt', 'w')

for i in range(0, len(players)):
    leaders_table.write(str(players[i]) + ' ' + str(scores[i]) + '\n')
pygame.quit()



