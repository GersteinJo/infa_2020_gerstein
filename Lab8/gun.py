from random import randrange as rnd, choice
from random import randint
import tkinter as tk
import math
import time

# print (dir(math))

root = tk.Tk()
fr = tk.Frame(root)
root.geometry('800x600')
canv = tk.Canvas(root, bg='white')
canv.pack(fill=tk.BOTH, expand=1)


class ball():
    def __init__(self, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.alive = True
        self.timelive = 5
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 10
        self.vy = 100
        self.color = choice(['blue', 'green', 'red', 'brown'])
        self.id = canv.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.color
        )
        self.live = 30

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
        # FIXME
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
        canv.delete(self.id)
        self.id = canv.create_oval( #put separately
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.color
        )
        
    def delete_ball(self):
        canv.delete(self.id)

    def hittest(obj, self):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        # FIXME
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + obj.r) ** 2:
            return True
        return False


class gun():
    def __init__(self):
        self.f2_power = 110
        self.f2_on = 0
        self.an = 1
        self.id = canv.create_line(20,450,50,420,width=7) # FIXME: don't know how to set it...
        self.score = 0
        self.id_score = canv.create_text(30,30,text = self.score,font = '28')

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = ball()
        new_ball.r += 5
        self.an = math.atan((event.y-new_ball.y) / (event.x-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 140

    def targetting(self, event=0):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.y-450) / (event.x-20))
        if self.f2_on:
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')
        canv.coords(self.id, 20, 450,
                    20 + max(self.f2_power, 20) * math.cos(self.an),
                    450 + max(self.f2_power, 20) * math.sin(self.an)
                    )

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 140:
                self.f2_power += 1
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')
            
    def hit_targ(self, targ, points = 10):
        canv.coords(targ.id, -10, -10, -10, -10) #удаляет с экрана(в смысле прячет)
        self.score += points #
        print(self.score)
        canv.delete(self.id_score)
        self.id_score = canv.create_text(30,30,text = self.score,font = '28')
        canv.itemconfig(self.id_score, text=self.score)
        


class target():      

    def new_target(self):
        """ Инициализация новой цели. """
        self.points = 0
        self.live = 1
    # FIXME: don't work!!! How to call this functions when object is created?
        self.id = canv.create_oval(0,0,0,0)
        x = self.x = rnd(600, 780)
        y = self.y = rnd(300, 550)
        r = self.r = rnd(20, 50)
        self.vx = rnd(-15,15)
        self.vy = rnd(-15,15)
        color = self.color = 'red'
        canv.coords(self.id, x-r, y-r, x+r, y+r)
        canv.itemconfig(self.id, fill=color)

    def hit(self, points=10):
        """Попадание шарика в цель."""
        canv.coords(self.id, -10, -10, -10, -10) #удаляет с экрана(в смысле прячет)
        self.points += points #
        canv.delete(self.id_points)
        canv.itemconfig(self.id_points, text=self.points)
        
    def move_targ(self):
        if self.x - self.r < 0 or self.x + self.r > 800:
            self.vx *= (-1)
            self.x += self.vx
        if self.y - self.r < 0 or self.y + self.r > 600:
            self.vy *= (-1)
            self.y -= self.vy
        self.y -= self.vy
        self.x += self.vx
        
        
    
    def draw_targ(self):
        x = self.x
        y = self.y
        r = self.r
        canv.coords(self.id, x-r, y-r, x+r, y+r)


t1 = target()
screen1 = canv.create_text(400, 300, text='', font='28')
g1 = gun()
bullet = 0
balls = []
targets = []

def new_game(event=''):
    global gun, t1, screen1, balls, bullet
    canv.itemconfig(screen1, text='')
    n = randint(2, 5)
    for i in range(n):
        t1 = target()
        t1.new_target()
        targets.append(t1)
    bullet = 0
    balls = []
    canv.bind('<Button-1>', g1.fire2_start)
    canv.bind('<ButtonRelease-1>', g1.fire2_end)
    canv.bind('<Motion>', g1.targetting)
    frame_period = 0.025

    z = 0.03
    while len(targets) > 0:# or balls:
        canv.bind('<Button-1>', g1.fire2_start)
        canv.bind('<ButtonRelease-1>', g1.fire2_end)
        canv.bind('<Motion>', g1.targetting)
        for targ in targets:
                targ.move_targ()
                targ.draw_targ()
        for b in balls:
            b.move()
            for targ in targets:
                if b.hittest(targ):
                    b.alive = False
                    g1.hit_targ(targ)
                    canv.bind('<Button-1>', '')
                    canv.bind('<ButtonRelease-1>', '')
                    targets.remove(targ)
            b.timelive -= frame_period
            if b.timelive < 0 or not (b.alive):
                print('aa')
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
    canv.itemconfig(screen1, text='You hit all the targets in ' + str(bullet) + ' shots')
    root.after(750, new_game)


new_game()

root.mainloop()
