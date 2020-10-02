import tkinter as tk
import pyautogui
import sys

SCREEN_W, SCREEN_H = pyautogui.size()

SIZE   = int(SCREEN_W*.25)
CENTER = int(SIZE/2)
BORDER = 2
RADIUS = int(CENTER - BORDER)

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

class Selector:
    def __init__(self, canvas):
        self.canvas = canvas
        # self.choices = [Choice(canvas) for _ in range(5)]

    def on_motion(self, e):
        canvas.itemconfig(self.selected, fill="blue")
        self.selected = canvas.find_closest(e.x, e.y)
        canvas.itemconfig(self.selected, fill="green")

    def draw(self, size):
        start = 90
        step = 360/size
        for i in range(size):
            self.canvas.create_circle_arc(CENTER, CENTER, RADIUS,
                                          start=start - i * step,
                                          extent=-step,
                                          fill="blue",
                                          outline="white",
                                          width=BORDER)
        self.selected = self.canvas.create_circle(CENTER, CENTER, SIZE * .15, fill="green", width=0)

        canvas.bind("<Motion>", lambda e: self.on_motion(e))

Selector(canvas).draw(5)

root.mainloop()