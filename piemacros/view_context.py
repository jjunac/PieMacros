import pyautogui

class ViewContext:
    @staticmethod
    def init():
        ViewContext.screen_size      = pyautogui.size()
        ViewContext.mouse_pos        = pyautogui.position()
        ViewContext.border_width     = 2
        ViewContext.window_size      = int(ViewContext.screen_size[0] * .23)
        ViewContext.window_center    = int(ViewContext.window_size / 2)
        ViewContext.selector_radius  = int(ViewContext.window_center - ViewContext.border_width)
        ViewContext.back_radius      = int(ViewContext.selector_radius * .3)
