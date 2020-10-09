# from math import *
from functools import wraps
import tkinter as tk

from .choice import BackChoice, Choice
from .constants import *
from .logging_utils import logger
from .view_context import ViewContext

@logger
class Selector:
    def __init__(self, choices):
        self._base_choices = choices
        for c in self._base_choices:
            c.set_selector(self)
        self._back_choice = BackChoice()
        self._back_choice.set_selector(self)
        self._choice_stack = []
        self._observers = set()

    def notify(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            res = func(*args, **kwargs)
            for o in args[0]._observers:
                o.on_selector_update()
        return wrapper

    def get_current_choices(self):
        # return self._base_choices
        return self._choice_stack[-1] if self._choice_stack else None

    def get_back_choice(self): return self._back_choice

    def subscribe(self, observer): self._observers.add(observer)

    def unsubscribe(self, observer): self._observers.remove(observer)

    @notify
    def reset_choices(self):
        if self._choice_stack:
            self._base_choices = self._choice_stack[0]
            self._choice_stack.clear()

    @notify
    def pop_choices(self):
        # if not self._choice_stack:
        #     self.hide()
        #     return
        # self._base_choices = self._choice_stack.pop()
        # self.draw()
        self._choice_stack.pop()

    @notify
    def push_choices(self, choices):
        # self._choice_stack.append(self._base_choices)
        # self._base_choices = choices
        # for c in self._base_choices:
        #     c.set_selector(self)
        # self.draw()
        self._choice_stack.append(choices)
        for c in self._choice_stack[-1]:
            c.set_selector(self)

    @notify
    def init_choices(self):
        self._choice_stack = [self._base_choices]

    # def add_choices(self, choices):
    #     for c in choices:
    #         self.add_choice(c)
    #     return self

    # def add_choice(self, choice):
    #     choice.set_selector(self)
    #     self._base_choices.append(choice)
    #     return self

    # def on_motion(self, e):
    #     curr_angle = atan2(e.y - ViewContext.window_center, e.x - ViewContext.window_center)
    #     if abs(cos(curr_angle)*ViewContext.back_radius) > abs(e.x - ViewContext.window_center):
    #         curr_choice = self._back_choice
    #     else:
    #         i = int(((degrees(curr_angle) + 90) / (360/len(self._base_choices)) + len(self._base_choices)) % len(self._base_choices))
    #         curr_choice = self._base_choices[i]

    #     if curr_choice != self._selected:
    #         self._selected.on_leave()
    #         self._selected = curr_choice
    #         self._selected.on_enter()

    # def on_click(self, e):
    #     self._logger.info("Choice selected: %s", self._selected.name)
    #     self._selected.execute()

    # def draw(self):
    #     self._logger.info("Drawing selector with choices %s", str([c.name for c in self._base_choices]))
    #     start = 90
    #     for i, c in enumerate(self._base_choices):
    #         idd = c.draw(i, len(self._base_choices))
    #     self._selected = self._back_choice
    #     self._back_choice.draw()

    # def show(self):
    #     ViewContext.init()

    #     self._root = tk.Tk()
    #     self.canvas = tk.Canvas(self._root,
    #                             width=ViewContext.window_size,
    #                             height=ViewContext.window_size,
    #                             highlightthickness=0,
    #                             bg="black")
    #     self.canvas.grid()

    #     self._root.overrideredirect(True)
    #     self._root.geometry(f"{ViewContext.window_size}"
    #                         f"x{ViewContext.window_size}"
    #                         f"+{ViewContext.mouse_pos[0] - ViewContext.window_center}"
    #                         f"+{ViewContext.mouse_pos[1] - ViewContext.window_center}")
    #     self._root.lift()
    #     self._root.wm_attributes("-topmost", True)
    #     # self._root.wm_attributes("-disabled", True)
    #     self._root.wm_attributes("-transparentcolor", "black")

    #     self.canvas.bind("<Escape>", self.hide)
    #     self.canvas.bind("<FocusOut>", self.hide)
    #     self.canvas.bind("<Motion>", self.on_motion)
    #     self.canvas.bind("<Button-1>", self.on_click)

    #     self.draw()
    #     self.canvas.focus_force()

    #     self._root.mainloop()

    # def hide(self, *args):
    #     self._logger.info("Closing selector")
    #     self.reset_choices()
    #     self._root.destroy()

