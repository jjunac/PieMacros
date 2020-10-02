import tkinter as tk

from action import *
from choice import *
from constants import *
from selector import Selector
import config
import tkutils

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

cp = config.ConfigParser("test_config.yaml").parse()

Selector(canvas).add_choices(cp.choices).draw()

root.mainloop()