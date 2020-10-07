import logging
from infi.systray import SysTrayIcon

from .action import *
from .choice import *
from .config import ConfigParser
from .constants import *
from .global_hotkey import GlobalHotkey, Modifiers
from .logging_utils import init_logging
from .selector import Selector
from .tkutils import decorate_tkinter

_selector = None
_systray = None

def run():
    init_logging()
    decorate_tkinter()

    cp = ConfigParser("test_config.yaml").parse()

    _selector = Selector().add_choices(cp.choices)
    # _selector.show()

    def about(systray):
        logging.info("About PieMacros...")

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
