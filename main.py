import tkinter as tk
import pyautogui
import sys
from math import *
import yaml
from pathlib import Path

SCREEN_W, SCREEN_H = pyautogui.size()

SIZE   = int(SCREEN_W*.25)
CENTER = int(SIZE/2)
BORDER = 2
RADIUS = int(CENTER - BORDER)

MATERIAL_COLORS = yaml.load(Path("material_colors.yaml").read_text())
SELECTOR_COLORS = ["red", "pink", "purple", "deepPurple", "indigo", "blue", "lightBlue", "cyan", "teal", "green", 
                   "lightGreen", "lime", "yellow", "amber", "orange", "deepOrange"]
mouse_pos = pyautogui.position()

root = tk.Tk()

canvas = tk.Canvas(root, width=SIZE, height=SIZE, highlightthickness=0, bg="black")
canvas.grid()

root.overrideredirect(True)
root.geometry(f"{SIZE}x{SIZE}+{int(mouse_pos[0] - CENTER)}+{int(mouse_pos[1] - CENTER)}")
root.lift()
root.wm_attributes("-topmost", True)
# root.wm_attributes("-disabled", True)
root.wm_attributes("-transparentcolor", "black")

root.bind('<Escape>', lambda e: exit(0))
root.bind("<FocusOut>", lambda e: exit(0))


def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x - r, y - r, x + r, y + r, **kwargs)
tk.Canvas.create_circle = _create_circle


def _create_circle_arc(self, x, y, r, **kwargs):
    if "start" in kwargs and "end" in kwargs:
        kwargs["extent"] = kwargs["end"] - kwargs["start"]
        del kwargs["end"]
    return self.create_arc(x - r, y - r, x + r, y + r, **kwargs)
tk.Canvas.create_circle_arc = _create_circle_arc

class Choice:
    def __init__(self, desc):
        self.desc = desc

    def draw(self, canvas, i, n):
        extent = -360/n
        start = 90 + i*extent
        self.canvas_id = canvas.create_circle_arc(CENTER, CENTER, RADIUS,
                                          start=start,
                                          extent=extent,
                                          fill=MATERIAL_COLORS[SELECTOR_COLORS[round(len(SELECTOR_COLORS)*i/n)]]["500"],
                                          outline="white",
                                          width=BORDER)
        text_pos = (CENTER + cos(radians(start + extent/2))*RADIUS*0.7, CENTER - sin(radians(start + extent/2))*RADIUS*0.7)
        print((i, *text_pos))
        canvas.create_text(*text_pos,
                           text=self.desc,
                           fill="white",
                           font=('Helvetica', '16'))
        return self.canvas_id

class Selector:
    def __init__(self, canvas):
        self.canvas = canvas
        self.choices = []
        self.id_to_choices = {}

    def add_choice(self, choice):
        self.choices.append(choice)
        return self

    def on_motion(self, e):
        canvas.itemconfig(self.selected, fill="blue")
        self.selected = canvas.find_closest(e.x, e.y)[0]
        canvas.itemconfig(self.selected, fill="green")

    def on_click(self, e):
        print(self.id_to_choices[self.selected].desc)

    def draw(self):
        start = 90
        for i, c in enumerate(self.choices):
            idd = c.draw(canvas, i, len(self.choices))
            self.id_to_choices[idd] = c
        self.selected = self.canvas.create_circle(CENTER, CENTER, SIZE * .15, fill="green", width=0)

        canvas.bind("<Motion>", lambda e: self.on_motion(e))
        canvas.bind("<Button-1>", lambda e: self.on_click(e))

Selector(canvas).add_choice(Choice("Test 1")) \
                .add_choice(Choice("Test 2")) \
                .add_choice(Choice("Test 3")) \
                .add_choice(Choice("Test 4")) \
                .add_choice(Choice("Test 5")) \
                .add_choice(Choice("Test 6")) \
                .draw()

root.mainloop()