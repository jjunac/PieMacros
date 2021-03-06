import logging
from infi.systray import SysTrayIcon

from .config import ConfigParser
from .global_hotkey import GlobalHotkey, Modifiers
from .logging_utils import init_logging
from .selector import Selector
from .theme import Theme
from .tkutils import decorate_tkinter
from .view import View

from .plugins import *

_selector = None
_systray = None
_view = None

def run():
    init_logging()
    decorate_tkinter()

    cp = ConfigParser("test_config.yaml").parse()

    Theme.set(cp.theme if cp.theme else "rainbow")

    _selector = Selector(cp.choices)
    _view = View(_selector)

    def about(systray):
        logging.info("About PieMacros...")

    menu_options = (('About PieMacros...', None, about),)

    _systray = SysTrayIcon(None, "PieMacros", menu_options, on_quit=lambda e: stop())
    _systray.start()

    GlobalHotkey.register('A', (Modifiers.WIN, Modifiers.SHIFT), _selector.init_choices)
    try:
        GlobalHotkey.listen()
    finally:
        stop()



def stop():
    GlobalHotkey.stop()
    GlobalHotkey.unregister_all()
    if _view: _view.hide()
    if _systray: _systray.shutdown()
