from choice import BackChoice, Choice
from constants import *
from math import *

class Selector:
    def __init__(self, canvas):
        self.canvas = canvas
        self.back_choice = BackChoice()
        self.back_choice.set_selector(self)
        self.choices = []
        self.choice_stack = []

    def add_choices(self, choices):
        for c in choices:
            self.add_choice(c)
        return self

    def add_choice(self, choice):
        choice.set_selector(self)
        self.choices.append(choice)
        return self
    
    def on_motion(self, e):
        curr_angle = atan2(e.y - CENTER, e.x - CENTER)
        if abs(cos(curr_angle)*BACK_RADIUS) > abs(e.x - CENTER):
            curr_choice = self.back_choice
        else:
            i = int(((degrees(curr_angle) + 90) / (360/len(self.choices)) + len(self.choices)) % len(self.choices))
            curr_choice = self.choices[i]

        if curr_choice != self.selected:
            self.selected.on_leave()
            self.selected = curr_choice
            self.selected.on_enter()

    def on_click(self, e):
        print(self.selected.name)
        self.selected.execute()

    def pop_choices(self):
        if not self.choice_stack:
            exit(0)
        self.choices = self.choice_stack.pop()
        self.draw()

    def push_choices(self, subchoices):
        self.choice_stack.append(self.choices)
        self.choices = subchoices
        for c in self.choices:
            c.set_selector(self)
        self.draw()

    def draw(self):
        start = 90
        for i, c in enumerate(self.choices):
            idd = c.draw(i, len(self.choices))
        self.selected = self.back_choice
        self.back_choice.draw()

        self.canvas.bind("<Motion>", lambda e: self.on_motion(e))
        self.canvas.bind("<Button-1>", lambda e: self.on_click(e))