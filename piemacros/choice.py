from math import *

from .constants import *
from .view_context import ViewContext

class Choice:
    def __init__(self, **kwargs):
        self.name = kwargs["name"]
        self.actions = kwargs.get("actions", None)

    def get_base_color(self): return self.color["400"]

    def get_accent_color(self): return self.color["A700"]

    def set_selector(self, selector): self.selector = selector

    def get_canvas(self): return self.selector.canvas

    def on_enter(self): self.get_canvas().itemconfig(self.canvas_id, fill=self.get_accent_color())

    def on_leave(self): self.get_canvas().itemconfig(self.canvas_id, fill=self.get_base_color())

    def draw(self, i, n):
        extent = -360/n
        start = 90 + i*extent
        self.color = MATERIAL_COLORS[SELECTOR_COLORS[round(len(SELECTOR_COLORS)*i/n)]]
        if n == 1:
            self.canvas_id = self.get_canvas().create_circle(ViewContext.window_center, ViewContext.window_center, ViewContext.selector_radius,
                                                             fill=self.get_base_color(),
                                                             outline="white",
                                                             width=ViewContext.border_width)
        else:
            self.canvas_id = self.get_canvas().create_circle_arc(ViewContext.window_center, ViewContext.window_center, ViewContext.selector_radius,
                                                                 start=start,
                                                                 extent=extent,
                                                                 fill=self.get_base_color(),
                                                                 outline="white",
                                                                 width=ViewContext.border_width)
        text_pos = (ViewContext.window_center + cos(radians(start + extent/2))*ViewContext.selector_radius*0.7, ViewContext.window_center - sin(radians(start + extent/2))*ViewContext.selector_radius*0.7)
        self.get_canvas().create_text(*text_pos,
                           text=self.name,
                           fill="white",
                           font=('Helvetica', '16'))
        return self.canvas_id

    def execute(self):
        self.selector.hide()
        for a in self.actions: a.execute()

class BackChoice(Choice):
    def __init__(self):
        Choice.__init__(self, name="Back", action=None)

    def draw(self):
        self.color = MATERIAL_COLORS["grey"]
        self.canvas_id = self.get_canvas().create_circle(ViewContext.window_center, ViewContext.window_center, ViewContext.back_radius, fill=self.get_base_color(), outline="white", width=ViewContext.border_width)
        return self.canvas_id

    def execute(self):
        self.selector.pop_choices()

    def get_accent_color(self):
        return self.color["600"]

class CompositeChoice(Choice):
    def __init__(self, **kwargs):
        Choice.__init__(self, **kwargs)
        self.subchoices = kwargs["subchoices"]

    def execute(self):
        self.selector.push_choices(self.subchoices)
