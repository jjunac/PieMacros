from math import *
import tkinter as tk

from .choice import BackChoice, Choice
from .constants import *
from .logging_utils import logger

@logger
class Selector:
    def __init__(self):
        self._back_choice = BackChoice()
        self._back_choice.set_selector(self)
        self._choices = []
        self._choice_stack = []

    def reset_choices(self):
        if self._choice_stack:
            self._choices = self._choice_stack[0]
            self._choice_stack.clear()

    def add_choices(self, choices):
        for c in choices:
            self.add_choice(c)
        return self

    def add_choice(self, choice):
        choice.set_selector(self)
        self._choices.append(choice)
        return self
    
    def on_motion(self, e):
        curr_angle = atan2(e.y - CENTER, e.x - CENTER)
        if abs(cos(curr_angle)*BACK_RADIUS) > abs(e.x - CENTER):
            curr_choice = self._back_choice
        else:
            i = int(((degrees(curr_angle) + 90) / (360/len(self._choices)) + len(self._choices)) % len(self._choices))
            curr_choice = self._choices[i]

        if curr_choice != self._selected:
            self._selected.on_leave()
            self._selected = curr_choice
            self._selected.on_enter()

    def on_click(self, e):
        self._logger.info("Choice selected: %s", self._selected.name)
        self._selected.execute()

    def pop_choices(self):
        if not self._choice_stack:
            self.hide()
            return
        self._choices = self._choice_stack.pop()
        self.draw()

    def push_choices(self, subchoices):
        self._choice_stack.append(self._choices)
        self._choices = subchoices
        for c in self._choices:
            c.set_selector(self)
        self.draw()

    def draw(self):
        self._logger.info("Drawing selector with choices %s", str([c.name for c in self._choices]))
        start = 90
        for i, c in enumerate(self._choices):
            idd = c.draw(i, len(self._choices))
        self._selected = self._back_choice
        self._back_choice.draw()

        self.canvas.bind("<Motion>", lambda e: self.on_motion(e))
        self.canvas.bind("<Button-1>", lambda e: self.on_click(e))

    def show(self):
        self._root = tk.Tk()

        self.canvas = tk.Canvas(self._root, width=SIZE, height=SIZE, highlightthickness=0, bg="black")
        self.canvas.grid()

        self._root.overrideredirect(True)
        self._root.geometry(f"{SIZE}x{SIZE}+{int(MOUSE_POS[0] - CENTER)}+{int(MOUSE_POS[1] - CENTER)}")
        self._root.lift()
        self._root.wm_attributes("-topmost", True)
        # self._root.wm_attributes("-disabled", True)
        self._root.wm_attributes("-transparentcolor", "black")

        self._root.bind('<Escape>', lambda e: self.hide())
        self._root.bind("<FocusOut>", lambda e: self.hide())

        self.draw()

        self._root.focus_force()

        self._root.mainloop()

    def hide(self):
        self._logger.info("Closing selector")
        self.reset_choices()
        self._root.destroy()

