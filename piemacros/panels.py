import pyautogui
from math import sin, cos, degrees, radians

from .geom_utils import GeomUtils
from .logging_utils import logger
from .theme import Theme

@logger
class SelectorPanel:
    def __init__(self, selector):
        self._selector = selector

    def on_motion(self, coor):
        self.hover_choice(coor)

    def on_click(self, coor):
        self.hover_choice(coor)
        self._selected_panel.on_click()

    def draw(self, canvas, ctx):
        self.canvas = canvas
        self.ctx = ctx
        self._choice_panels = []
        self._back_choice_panel = None
        self._logger.info("Drawing selector with choices %s", str([c.name for c in self._selector.get_current_choices()]))
        start = 90
        nb_choices = len(self._selector.get_current_choices())
        extent = 360 / nb_choices
        for i, c in enumerate(self._selector.get_current_choices()):
            start -= extent
            cp = ChoicePanel(c, Theme.get().get_choice_color(i, nb_choices))
            cp.draw(canvas, ctx, start, extent)
            self._choice_panels.append(cp)
        self._back_choice_panel = BackChoicePanel(self._selector.get_back_choice(), Theme.get().get_back_color())
        self._back_choice_panel.draw(canvas, ctx)

        self._selected_panel = None

        abs_mouse_pos = pyautogui.position()
        self.hover_choice((abs_mouse_pos[0] - self.canvas.master.winfo_rootx(), abs_mouse_pos[1] - self.canvas.master.winfo_rooty()))


    def hover_choice(self, coor):
        curr_angle = GeomUtils.coor_to_angle(coor, (self.ctx.window_center, self.ctx.window_center))
        if GeomUtils.are_polar_coor_inside_circle(coor[0] - self.ctx.window_center, curr_angle, self.ctx.back_radius):
            curr_choice_panel = self._back_choice_panel
        else:
            curr_choice_panel = self._choice_panels[GeomUtils.current_circle_subdivision(curr_angle, len(self._choice_panels))]

        if curr_choice_panel != self._selected_panel:
            if self._selected_panel:
                self._selected_panel.on_leave()
            self._selected_panel = curr_choice_panel
            self._selected_panel.on_enter()


@logger
class ChoicePanel:
    def __init__(self, choice, theme):
        self._choice = choice
        self._theme = theme

    def on_enter(self): self._canvas.itemconfig(self._canvas_id, fill=self._theme.accent_color)

    def on_leave(self): self._canvas.itemconfig(self._canvas_id, fill=self._theme.base_color)

    def on_click(self):
        self._logger.info("Choice selected: %s", self._choice.name)
        self._choice.execute()

    def draw(self, canvas, ctx, start, extent):
        self._canvas = canvas
        self.ctx = ctx
        self._canvas_id = self._canvas.create_circle_arc(ctx.window_center, ctx.window_center, ctx.selector_radius,
                                                        start=start,
                                                        extent=extent,
                                                        fill=self._theme.base_color,
                                                        outline="white",
                                                        width=ctx.border_width)
        text_pos = (ctx.window_center + cos(radians(start + extent/2))*ctx.selector_radius*0.7, ctx.window_center - sin(radians(start + extent/2))*ctx.selector_radius*0.7)
        self._canvas.create_text(*text_pos,
                           text=self._choice.name,
                           fill="white",
                           font=('Helvetica', '14'))


@logger
class BackChoicePanel(ChoicePanel):
    def __init__(self, choice, theme):
        ChoicePanel.__init__(self, choice, theme)

    def draw(self, canvas, ctx):
        self._canvas = canvas
        self.ctx = ctx
        self._canvas_id = self._canvas.create_circle(ctx.window_center, ctx.window_center, ctx.back_radius,
                                                    fill=self._theme.base_color,
                                                    outline="white",
                                                    width=self.ctx.border_width)

