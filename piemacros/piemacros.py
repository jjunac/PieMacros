import logging
from infi.systray import SysTrayIcon

from .action import *
from .choice import *
from .constants import *
from .selector import Selector
from .config import ConfigParser
from .tkutils import decorate_tkinter
from .global_hotkey import GlobalHotkey, Modifiers

_selector = None
_systray = None

def run():
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

    decorate_tkinter()

    cp = ConfigParser("test_config.yaml").parse()

    _selector = Selector().add_choices(cp.choices)
    # _selector.show()

    def about(systray):
        print("About")

    menu_options = (('About PieMacros...', None, about),)

    _systray = SysTrayIcon(None, "PieMacros", menu_options, on_quit=lambda e: stop())
    _systray.start()

    GlobalHotkey.register('A', (Modifiers.WIN, Modifiers.SHIFT), lambda: _selector.show())
    try:
        GlobalHotkey.listen()
    finally:
        stop()



def stop():
    GlobalHotkey.stop()
    GlobalHotkey.unregister_all()
    if _selector: _selector.hide()
    if _systray: _systray.shutdown()
