from tkinter import *  # импорт GUI модуля
import random
import pygame

# Глобальные
WIDTH = 800
HEIGHT = 600
SEG_SIZE = 20 # размер сегмента змеи
IN_GAME = True # состояние игры


# вспомогательные функции
def create_block():
    """ яблоко """
    global BLOCK
    posx = SEG_SIZE * random.randint(1, (WIDTH-SEG_SIZE) / SEG_SIZE)
    posy = SEG_SIZE * random.randint(1, (HEIGHT-SEG_SIZE) / SEG_SIZE)
    BLOCK = c.create_oval(posx, posy,
                          posx+SEG_SIZE, posy+SEG_SIZE,
                          fill="red")


def main():
    """ управление игровым процессом """
    global IN_GAME
    if IN_GAME:
        s.move() # двигаем змейку
        head_coords = c.coords(s.segments[-1].instance) # определяем координаты головы
        x1, y1, x2, y2 = head_coords
        # столкновение с границей
        if x2 > WIDTH or x1 < 0 or y1 < 0 or y2 > HEIGHT:
            IN_GAME = False
        # поедание яблок
        elif head_coords == c.coords(BLOCK):
            s.add_segment()
            c.delete(BLOCK)
            create_block()
        # поедание себя
        else:
            for index in range(len(s.segments)-1):
                if head_coords == c.coords(s.segments[index].instance):
                    IN_GAME = False
        root.after(100, main)
    # если всё, то печатать
    else:
        c.create_text(WIDTH/2, HEIGHT/2,
                      text="Сложнааа, блеать",
                      font="Arial 30",
                      fill="Red")


class Segment(object):
    def __init__(self, x, y):
        self.instance = c.create_rectangle(x, y,
                                           x+SEG_SIZE, y+SEG_SIZE,
                                           fill="#7FFF00")


class Snake(object):
    def __init__(self, segments):
        self.segments = segments
        # возможные направления движения
        self.mapping = {"Down": (0, 1), "Right": (1, 0),
                        "Up": (0, -1), "Left": (-1, 0)}
        # начальное движение
        self.vector = self.mapping["Right"]

    def move(self):
        """
        двигаем змею в нужном направлении. Перебираем все сегменты, кроме первого.
        какая-то хуета, можно проще, доработать потом --->
        """
        for index in range(len(self.segments)-1):
            segment = self.segments[index].instance
            x1, y1, x2, y2 = c.coords(self.segments[index+1].instance)
            c.coords(segment, x1, y1, x2, y2)

        x1, y1, x2, y2 = c.coords(self.segments[-2].instance)
        c.coords(self.segments[-1].instance,
                 x1+self.vector[0]*SEG_SIZE, y1+self.vector[1]*SEG_SIZE,
                 x2+self.vector[0]*SEG_SIZE, y2+self.vector[1]*SEG_SIZE)

    def add_segment(self):
        """ добавляем сегмент питону:)"""
        last_seg = c.coords(self.segments[0].instance)
        x = last_seg[2] - SEG_SIZE
        y = last_seg[3] - SEG_SIZE
        self.segments.insert(0, Segment(x, y))

    def change_direction(self, event):
        """ изменение направления движения """
        if event.keysym in self.mapping:
            self.vector = self.mapping[event.keysym]





# билдим окно
root = Tk()
root.title("Питон на питоне кароч:)")

# создаем экземпляр класса канвас и заливаем цветом
c = Canvas(root, width=WIDTH, height=HEIGHT, bg="#7FFFD4")
c.grid()
# ловим нажатия
c.focus_set()
# создаем набор начальных сегментов
segments = [Segment(SEG_SIZE, SEG_SIZE),
            Segment(SEG_SIZE*2, SEG_SIZE),
            Segment(SEG_SIZE*3, SEG_SIZE)]
# змейка кароч
s = Snake(segments)
# обработка нажатий клавиш
c.bind("<KeyPress>", s.change_direction)


# билдим элементы и запускаем окно
create_block()
main()
root.mainloop()
