from random import randrange as rnd, choice
from random import randint
from random import random
import tkinter as tk
import math
import time

# print (dir(math))

root = tk.Tk()
fr = tk.Frame(root)
root.geometry('800x600')
canv = tk.Canvas(root, bg='white')
canv.pack(fill=tk.BOTH, expand=1)
canv.focus_set()


class ball():
    def __init__(self, r, x=40, y=450, vx = 10, vy = 100, hitter = False):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.alive = True
        self.timelive = 2
        self.x = x
        self.y = y
        self.r = r
        self.vx = vx
        self.vy = vy
        self.color = 'black'#choice(['blue', 'green', 'black', 'brown'])
        self.id = canv.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.color
        )
        self.live = 30
        self.hitter = hitter

    def set_coords(self):
        canv.coords(
                self.id,
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r
        )

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        g = 5
        if self.x - self.r < 0 or self.x + self.r > 800:
            self.vx *= (-1)
            self.x += self.vx
        if self.y - self.r < 0 or self.y + self.r > 600:
            self.vy *= (-1)
            self.y -= self.vy
        self.vx *= 0.9
        self.vy *= 0.9
        self.vy -= g
        self.x += self.vx
        self.y -= self.vy
        canv.coords(self.id, self.x - self.r, self.y - self.r, self.x+self.r, self.y+self.r)
        canv.itemconfig(self.id, fill=self.color)
        
        
    def delete_ball(self):
        '''
        deletes image of a ball
        '''
        canv.delete(self.id)

    def hittest(obj, self):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """

        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + obj.r) ** 2:
            return True
        return False


class gun():
    def __init__(self, x = 20, y = 450):
        self.x = x
        self.y = y
        self.f2_power = 140
        self.f2_on = 0
        self.an = 1
        self.id = canv.create_line(self.x, self.y, 50, 420, width=7)
        self.score = 0
        self.id_score = canv.create_text(30, 30,text = self.score,font = '28')
        self.laser_id = canv.create_line(self.x + 30, self.y - 30, 0, 0, width=2)
        self.mousepos = []
        self.used_laser = False
        

    def fire2_start(self, event = ''):
        '''
        turns the gun on

        '''
        self.f2_on = 1

    def fire2_end(self, event = ''):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = ball(30 / 140 * self.f2_power, self.x + 10, self.y + 15)
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 90

    def targetting(self, event=0):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            if not (event.x-self.x == 0):
                self.an = math.atan((event.y-self.y) / (event.x-self.x))
            elif event.y-self.y > 0:
                self.an = float(math.pi/2)
            else:
                self.an = - float(math.pi/2)
                
        if self.f2_on:
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')
        canv.coords(self.id, self.x, self.y,
                    self.x + max(self.f2_power, 20) * math.cos(self.an),
                    self.y + max(self.f2_power, 20) * math.sin(self.an)
                    )

    def power_up(self):
        '''
        this one draws the gun
        also if mousebutton is down it raises power of a strike

        Returns
        -------
        None.

        '''
        if self.f2_on:
            if self.f2_power < 140:
                self.f2_power += 5
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')        
            
    def hit_targ(self, targ, points = 10):
        '''
        if the target is hit, deletes target and add score
        targ : object of collision
        points : amount of points given for the kill
        '''
        canv.delete(targ.id)
        self.score += points #
        print(self.score)
        canv.delete(self.id_score)
        self.id_score = canv.create_text(30,30,text = self.score,font = '28')
        canv.itemconfig(self.id_score, text=self.score)
        
    def move(self, event = ''):
        print('up I go')
        if event.keysym == 'Up' and self.y > 100:
            self.y -= 2  
        elif event.keysym == 'Down' and self.y < 500:
            self.y += 2
        elif event.keysym == 'Left' and self.x > 10:
            self.x -= 2  
        elif event.keysym == 'Right' and self.x < 400:
            self.x += 2
        
    def check_being_hit(self, da_ball, points = 10):
        if (da_ball.x > min(self.x, self.x + max(self.f2_power, 20) * math.cos(self.an))
        and da_ball.x < max(self.x, self.x + max(self.f2_power, 20) * math.cos(self.an))
        and da_ball.y > min(self.y, self.y + max(self.f2_power, 20) * math.sin(self.an))
        and da_ball.y < max(self.y, self.y + max(self.f2_power, 20) * math.sin(self.an))):
            self.score -= points
            canv.delete(self.id_score)
            self.id_score = canv.create_text(30,30,text = self.score,font = '28')
            canv.itemconfig(self.id_score, text=self.score)
            return True
        return False
        
    def not_a_laser_strike(self, event = 0):
        self.used_laser = True
        self.mousepos = []
        if event:    
            self.mousepos.append(event.x)
            self.mousepos.append(event.y)
            canv.itemconfig(self.laser_id, fill = 'red')
            canv.coords(self.laser_id, self.x, self.y, event.x, event.y)
    
    def check_not_laser_strike(self, targ):
        mx, my = self.mousepos[0], self.mousepos[1]
        tx, ty = targ.x, targ.y
        sx, sy = self.x, self.y
        ms = ((mx - sx) ** 2 + (my - sy) ** 2) ** 0.5
        mt = ((mx - tx) ** 2 + (my - ty) ** 2) ** 0.5
        ts = ((tx - sx) ** 2 + (ty - sy) ** 2) ** 0.5
        p = (ms + mt + ts) / 2
        seekdist = (p * (p - ms) * (p - mt) * (p - ts)) ** 0.5 / 2 / ms
        if seekdist < targ.r:
            return True
        return False
    
    def off_laser(self):
        canv.coords(self.laser_id, self.x, self.y, self.x, self.y)
        self.used_laser = False


class target():      

    def __init__(self, x = -1, y = -1, r = -1, vx = 0, vy = 0, color = 'red', falling = False, ID = None):
        self.points = 0
        self.live = 1
        self.id = ID
        if x == -1:
            x = self.x = rnd(600, 780)
        else:
            self.x = x
        if y == -1:
            y = self.y = rnd(100, 300)
        else:
            self.y = y
        if r == -1:
            r = self.r = rnd(20, 35)
        else:
            self.r = r
        if vx == 0:
            vx = self.vx = rnd(-15, 15)
        else:
            self.vx = vx
        if vy == 0:
            vy = self.vy = rnd(-15, 15)
        else:
            self.vy = vy
        
        self.color = color
        
        self.falling = falling
        canv.coords(self.id, x-r, y-r, x+r, y+r)
        canv.itemconfig(self.id, fill=color)

    def hit(self, points=10):
        """Попадание шарика в цель."""
        return None, None
        
    def move_targ(self):
        '''
        Moves the target

        Returns
        -------
        None.

        '''
        g = 5
        if self.falling:
            self.vy -= g
            self.vy *= 0.9
        if self.x - self.r < 0 or self.x + self.r > 800:
            self.vx *= (-1)
            self.x += self.vx
        if self.y - self.r < 0 or self.y + self.r > 600:
            self.vy *= (-1)
            self.y -= self.vy
        self.y -= self.vy
        self.x += self.vx      
    
    def draw_targ(self):
        '''
        Draws the target

        Returns
        -------
        None.

        '''
        x = self.x
        y = self.y
        r = self.r
        canv.coords(self.id, x-r, y-r, x+r, y+r)
        canv.itemconfig(self.id, fill=self.color)
        
    def act(self):
        return None
        
        
class grape_shot(target):
    def hit(self, points = 15):
        """Попадание шарика в цель."""
        v_rel = 10
        t1 = target(self.x, self.y, self.r / 2, self.vx + v_rel * 2, self.vy + v_rel, 'purple', True, ID = canv.create_oval(0,0,0,0))
        t2 = target(self.x, self.y, self.r / 2, self.vx - v_rel * 2, self.vy - v_rel, 'purple', True, ID = canv.create_oval(0,0,0,0))
        return t1, t2

class bombarder(target):
    def move_targ(self):
        if self.x - self.r < 0 or self.x + self.r > 800:
            self.vx *= (-1)
        self.x += self.vx  
    
    def act(self):
        b = ball(10, self.x, self.y, 0, 0, True)
        return b
        
        
        

def new_game(event=''):
    global gun, screen1, balls, bullet
    hurt = 0
    canv.delete(tk.ALL)
    screen1 = canv.create_text(400, 300, text='', font='28')
    g1 = gun()
    bullet = 0
    balls = []
    targets = []
    canv.itemconfig(screen1, text='')
    n = randint(2, 5)
    for i in range(n):
        t1 = target(ID = canv.create_oval(0, 0, 0, 0))
        targets.append(t1)
    for i in range(n - 2):
        gr_sh = grape_shot(color = 'yellow', ID = canv.create_oval(0, 0, 0, 0))
        targets.append(gr_sh)
    for i in range (2):
        bomb = bombarder(color = 'blue', ID = canv.create_rectangle(0, 0, 0, 0))
        targets.append(bomb)
    bullet = 0
    balls = []
    canv.bind('<Button-1>', g1.fire2_start)
    canv.bind('<ButtonRelease-1>', g1.fire2_end)
    canv.bind('<Motion>', g1.targetting)
    canv.bind('<Button-3>', g1.not_a_laser_strike)
    canv.bind('<KeyPress>', g1.move)
              
    frame_period = 0.025

    z = 0.03
    while len(targets) > 0:
        
        canv.bind('<Button-1>', g1.fire2_start)
        canv.bind('<ButtonRelease-1>', g1.fire2_end)
        canv.bind('<Motion>', g1.targetting)
        canv.bind('<Button-3>', g1.not_a_laser_strike)
        canv.bind('<KeyPress>', g1.move)
        for targ in targets:
            if random() < 0.05:
                b1 = targ.act()
                if not(b1 == None):
                    balls.append(b1)
            targ.move_targ()
            targ.draw_targ()
            if g1.used_laser:
                if g1.check_not_laser_strike(targ):
                    g1.hit_targ(targ, points = 2)
                    targets.remove(targ)
                    bullet += 1
        g1.off_laser()            
        for b in balls:
            b.move()
            if b.hitter:
                if g1.check_being_hit(b):
                    hurt += 1
            else:
                for targ in targets:
                    if b.hittest(targ):
                        b.alive = False
                        g1.hit_targ(targ)
                        canv.bind('<Button-1>', '')
                        canv.bind('<ButtonRelease-1>', '')
                        tag1, tag2 = targ.hit()
                        if not(tag1 == None):
                            targets.append(tag1)
                            targets.append(tag2)
                        targets.remove(targ)
            b.timelive -= frame_period
            if b.timelive < 0 or not (b.alive):
                b.delete_ball()
                balls.remove(b)
        canv.update()
        g1.targetting()
        g1.power_up()        
        time.sleep(frame_period)
    canv.itemconfig(screen1, text='')
    canv.delete(gun)
    for b in balls:
        b.delete_ball()
        balls.remove(b)
    canv.itemconfig(screen1, text='You hit all the targets in ' + str(bullet) + ' shots \n And has been hit ' 
                    + str(hurt) + ' times')
    root.after(1000, new_game)

new_game()

root.mainloop()
