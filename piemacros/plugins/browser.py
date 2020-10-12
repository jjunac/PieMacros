import webbrowser

from ..action import Action, register_action

@register_action("browser.new_tab")
class BrowserNewTabAction(Action):
    def __init__(self, args):
        self.url = args

    def execute(self):
        webbrowser.get('firefox').open_new_tab(self.url)