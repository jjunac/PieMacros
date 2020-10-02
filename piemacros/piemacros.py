import tkinter as tk

import tkutils
from action import *
from choice import *
from selector import Selector
from constants import *

tkutils.decorate()

root = tk.Tk()

canvas = tk.Canvas(root, width=SIZE, height=SIZE, highlightthickness=0, bg="black")
canvas.grid()

root.overrideredirect(True)
root.geometry(f"{SIZE}x{SIZE}+{int(MOUSE_POS[0] - CENTER)}+{int(MOUSE_POS[1] - CENTER)}")
root.lift()
root.wm_attributes("-topmost", True)
# root.wm_attributes("-disabled", True)
root.wm_attributes("-transparentcolor", "black")

root.bind('<Escape>', lambda e: exit(0))
root.bind("<FocusOut>", lambda e: exit(0))

subchoices = [
    Choice(name="Test 1", action=create_action("alert", "hello")),
    Choice(name="Test 2", action=create_action("move mouse", "200,200"))
]

Selector(canvas).add_choice(Choice(name="Test 1", action=create_action("alert", "hello"))) \
                .add_choice(Choice(name="Test 2", action=create_action("move mouse", "200,200"))) \
                .add_choice(CompositeChoice(name="Test 3", action=None, subchoices=subchoices)) \
                .add_choice(Choice(name="Test 4", action=create_action("alert", "hello"))) \
                .add_choice(Choice(name="Test 5", action=create_action("alert", "hello"))) \
                .add_choice(Choice(name="Test 6", action=create_action("alert", "hello"))) \
                .draw()

root.mainloop()