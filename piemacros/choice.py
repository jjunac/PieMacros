from math import *

from .constants import *

class Choice:
    def __init__(self, **kwargs):
        self.name = kwargs["name"]
        self.action = kwargs.get("action", None)

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
        self.canvas_id = self.get_canvas().create_circle_arc(CENTER, CENTER, RADIUS,
                                                       start=start,
                                                       extent=extent,
                                                       fill=self.get_base_color(),
                                                       outline="white",
                                                       width=BORDER)
        text_pos = (CENTER + cos(radians(start + extent/2))*RADIUS*0.7, CENTER - sin(radians(start + extent/2))*RADIUS*0.7)
        self.get_canvas().create_text(*text_pos,
                           text=self.name,
                           fill="white",
                           font=('Helvetica', '16'))
        return self.canvas_id

    def execute(self):
        self.action.execute()
        self.selector.hide()

class BackChoice(Choice):
    def __init__(self):
        Choice.__init__(self, name="Back", action=None)

    def draw(self):
        self.color = MATERIAL_COLORS["grey"]
        self.canvas_id = self.get_canvas().create_circle(CENTER, CENTER, SIZE*.15, fill=self.get_base_color(), outline="white", width=BORDER)
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
