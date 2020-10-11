from dataclasses import dataclass
import pyautogui
import tkinter as tk

from .logging_utils import logger
from .panels import SelectorPanel

@logger
class View:
    @dataclass
    class Context:
        def __init__(self, screen_size, mouse_pos):
            self.screen_size      = screen_size
            self.mouse_pos        = mouse_pos
            self.border_width     = 2
            self.window_size      = int(self.screen_size[0] * .23)
            self.window_center    = int(self.window_size / 2)
            self.selector_radius  = int(self.window_center - self.border_width)
            self.back_radius      = int(self.selector_radius * .3)


    def __init__(self, selector):
        self._selector = selector
        self._selector.subscribe(self)
        self._selector_panel = SelectorPanel(self._selector)
        self._root = None

    def draw(self):
        self.canvas.delete("all")
        self._selector_panel.draw(self.canvas, self.ctx)

    def on_motion(self, e):
        self._selector_panel.on_motion((e.x, e.y))

    def on_click(self, e):
        self._selector_panel.on_click((e.x, e.y))

    def on_selector_update(self):
        if self._selector.get_current_choices() is not None:
            if self._root:
                self.draw()
            else:
                self.show()
        else:
            self.hide()

    def show(self):
        self.ctx = View.Context(pyautogui.size(), pyautogui.position())
        self._root = tk.Tk()
        self.canvas = tk.Canvas(self._root,
                                width=self.ctx.window_size,
                                height=self.ctx.window_size,
                                highlightthickness=0,
                                bg="black")
        self.canvas.grid()

        self._root.overrideredirect(True)
        self._root.geometry(f"{self.ctx.window_size}"
                            f"x{self.ctx.window_size}"
                            f"+{self.ctx.mouse_pos[0] - self.ctx.window_center}"
                            f"+{self.ctx.mouse_pos[1] - self.ctx.window_center}")
        self._root.lift()
        self._root.wm_attributes("-topmost", True)
        # self._root.wm_attributes("-disabled", True)
        self._root.wm_attributes("-transparentcolor", "black")

        self.canvas.bind("<Escape>", self.hide)
        self.canvas.bind("<FocusOut>", self.hide)
        self.canvas.bind("<Motion>", self.on_motion)
        self.canvas.bind("<Button-1>", self.on_click)

        self.draw()
        self.canvas.focus_force()

        self._root.mainloop()


    def hide(self, *args):
        if self._root:
            self._logger.info("Closing selector")
            self._root.destroy()
            self._root = None


