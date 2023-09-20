import csv
import tkinter as tk
from tkinter import Tk, Canvas, Frame, BOTH
from pynput import keyboard


class Field:
    __colors = {'w': 'red', 'g': 'green'}

    def __init__(self, x1, y1, x2, y2, pt):
        self.x1 = x1
        self.y1 = y1
        self.y2 = y2
        self.x2 = x2
        self.pt = pt

    def color(self):
        return self.__colors[self.pt]


class Area:
    def __init__(self, fields_list, rows, cols):
        self.area = fields_list
        self.rows = rows
        self.cols = cols

    def get_ground_fields(self):
        return [f for f in self.area if f.pt == 'g']

    def by_id(self, id):
        return self.area[id]


def init_map2():
    map = []
    with open('map-test.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        size = 10
        rows = 0
        cols = 1
        for n, row in enumerate(reader, start=1):
            rows += 1
            cols = len(row)
            for ii, rr in enumerate(row, start=1):
                field = Field((ii - 1) * size, (n - 1) * size, ii * size, n * size, rr)
                map.append(field)

    return Area(map, rows, cols)


class Player:
    # ToDo [ ] Отрефачить этот ужОс!
    def __init__(self, area: Area, color, canvas, d):
        self.pos = 0
        self.area = area
        self.color = color
        self.canvas = canvas
        self.d = d
        self.is_over = False

    def __check_position(self, pos):
        f = self.area.by_id(pos)
        if f.pt == 'w':
            return False
        return True

    def looser(self):
        self.is_over = True
        for dd in self.d:
            self.canvas.itemconfig(dd, fill='white', outline='white')
        self.canvas.create_text(100, 100,
              text="Ты проебал",
              justify=tk.CENTER, font="Verdana 14")

    def get_start_position(self):
        for i, el in enumerate(self.area.area):
            if el.pt != 'w':
                self.pos = i
                return i

    def move_r(self):
        if not self.is_over:

            field = self.area.by_id(self.pos)
            self.canvas.itemconfig(self.d[self.pos], fill=field.color())
            if self.pos + 1 <= len(self.area.area) - 1:
                self.pos += 1
            else:
                self.pos = 0
            if not self.__check_position(self.pos):
                self.looser()
            return self.pos
        self.looser()

    def move_l(self):
        if not self.is_over:
            field = self.area.by_id(self.pos)
            self.canvas.itemconfig(self.d[self.pos], fill=field.color())
            if self.pos - 1 >= 0:
                self.pos -= 1
            else:
                self.pos = len(self.area.area) - 1
            if not self.__check_position(self.pos):
                self.looser()
            return self.pos
        self.looser()

    def move_t(self):
        if not self.is_over:
            area_count = int(self.area.cols*self.area.rows)
            field = self.area.by_id(self.pos)
            self.canvas.itemconfig(self.d[self.pos], fill=field.color())
            if self.pos - self.area.cols < 0:
                self.pos = area_count - (self.area.cols - self.pos)
            else:
                self.pos -= self.area.cols
            if not self.__check_position(self.pos):
                self.looser()
            return self.pos
        self.looser()

    def move_d(self):
        if not self.is_over:
            area_count = int(self.area.cols*self.area.rows)
            field = self.area.by_id(self.pos)
            self.canvas.itemconfig(self.d[self.pos], fill=field.color())
            if self.pos + self.area.cols > area_count:
                print('----------------------------------')
                self.pos = self.area.cols + (self.pos - area_count)
            else:
                self.pos += self.area.cols
            if not self.__check_position(self.pos):
                self.looser()
            return self.pos
        self.looser()



def event_info(event):
    """Отладочное говно!"""
    print(type(event))
    print(event)
    print(event.time)
    print(event.x_root)
    print(event.y_root)


def main():
    root = Tk()
    root.geometry("1200x800")
    root.title('Рисуем поле')
    canvas = tk.Canvas(root, width=1200, height=800)
    area = init_map2()
    # ToDo [ ] Обернуть эту дрочь в класс!
    d = {}
    # рисуем поле
    for i, el in enumerate(area.area):
        o = canvas.create_rectangle(
            el.x1, el.y1, el.x2, el.y2,
            fill=el.color(), outline='black', width=2
        )
        d[i] = o
    # ставим игрока
    p = Player(area, 'yellow', canvas, d)
    canvas.itemconfig(d[p.get_start_position()], fill=p.color)
    canvas.pack()
    root.bind('d', lambda x: canvas.itemconfig(d[p.move_r()], fill=p.color))
    root.bind('a', lambda x: canvas.itemconfig(d[p.move_l()], fill=p.color))
    root.bind('w', lambda x: canvas.itemconfig(d[p.move_t()], fill=p.color))
    root.bind('s', lambda x: canvas.itemconfig(d[p.move_d()], fill=p.color))
    root.mainloop()


if __name__ == '__main__':
    main()


