import logging

from .action import *
from .choice import *
from .constants import *
from .selector import Selector
from .config import ConfigParser
from .tkutils import decorate_tkinter
from .global_hotkey import GlobalHotkey, Modifiers

_selector = None

def run():
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

    decorate_tkinter()

    cp = ConfigParser("test_config.yaml").parse()

    _selector = Selector().add_choices(cp.choices)
    # _selector.show()
    GlobalHotkey.register('A', (Modifiers.WIN, Modifiers.SHIFT), lambda: _selector.show())
    try:
        GlobalHotkey.listen()
    finally:
        GlobalHotkey.unregister_all()



# def stop():
#     _selector.hide()
