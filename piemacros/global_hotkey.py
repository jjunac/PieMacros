'''
From http://timgolden.me.uk/python/win32_how_do_i/catch_system_wide_hotkeys.html
'''
from ctypes import wintypes
from enum import IntEnum
import ctypes
import itertools
import win32con
import time

from .logging_utils import logger

byref = ctypes.byref
user32 = ctypes.windll.user32


class Modifiers(IntEnum):
    SHIFT   = win32con.MOD_SHIFT
    ALT     = win32con.MOD_ALT
    CONTROL = win32con.MOD_CONTROL
    WIN     = win32con.MOD_WIN

@logger
class GlobalHotkey:
    _hotkey_id = itertools.count(1)
    _callbacks = {}
    _listening = False

    @staticmethod
    def register(key, modifiers, callback):
        # RegisterHotKey takes:
        #  Window handle for WM_HOTKEY messages (None = this thread)
        #  arbitrary id unique within the thread
        #  modifiers (MOD_SHIFT, MOD_ALT, MOD_CONTROL, MOD_WIN)
        #  VK code (either ord ('x') or one of win32con.VK_*)
        id = next(GlobalHotkey._hotkey_id)
        GlobalHotkey._logger.info(f"Registering global hotkey [{id}] with key={key}, modifiers={modifiers}")
        registered = user32.RegisterHotKey(None, id, sum(modifiers), ord(key))
        if not registered:
            GlobalHotkey._logger.error(f"Unable to register [{id}]")
            return -1
        GlobalHotkey._callbacks[id] = callback
        return id

    @staticmethod
    def stop():
        GlobalHotkey._listening = False


    @staticmethod
    def listen():
        # Home-grown Windows message loop: does
        #  just enough to handle the WM_HOTKEY
        #  messages and pass everything else along.
        msg = wintypes.MSG()
        GlobalHotkey._listening = True
        while GlobalHotkey._listening:
            time.sleep(0.1)
            retrieved = user32.PeekMessageA(byref(msg), None, win32con.WM_HOTKEY, win32con.WM_HOTKEY, win32con.PM_REMOVE)
            if not retrieved:
                continue

            if msg.wParam in GlobalHotkey._callbacks:
                GlobalHotkey._logger.info(f"Callback [{msg.wParam}] triggered")
                GlobalHotkey._callbacks[msg.wParam]()

            # Pass on to the next global listener
            user32.TranslateMessage(byref(msg))
            user32.DispatchMessageA(byref(msg))

    @staticmethod
    def unregister_all():
        for id in GlobalHotkey._callbacks:
            GlobalHotkey.unregister(id)
    
    @staticmethod
    def unregister(id):
        GlobalHotkey._logger.info(f"Unregistering global hotkey [{id}]")
        user32.UnregisterHotKey(None, id)