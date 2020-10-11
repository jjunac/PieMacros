import tkinter as tk


def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x - r, y - r, x + r, y + r, **kwargs)


def _create_circle_arc(self, x, y, r, **kwargs):
    if "start" in kwargs and "end" in kwargs:
        kwargs["extent"] = kwargs["end"] - kwargs["start"]
        del kwargs["end"]
    if kwargs["extent"] != 0 and kwargs["extent"] % 360 == 0:
        del kwargs["start"], kwargs["extent"]
        return self.create_circle(x, y, r, **kwargs)
    return self.create_arc(x - r, y - r, x + r, y + r, **kwargs)

def decorate_tkinter():
    tk.Canvas.create_circle = _create_circle
    tk.Canvas.create_circle_arc = _create_circle_arc
