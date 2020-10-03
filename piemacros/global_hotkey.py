'''
From http://timgolden.me.uk/python/win32_how_do_i/catch_system_wide_hotkeys.html
'''
from ctypes import wintypes
from enum import IntEnum
import ctypes
import itertools
import logging
import os
import sys
import win32con

byref = ctypes.byref
user32 = ctypes.windll.user32

HOTKEYS = {
1 : (ord('A'), win32con.MOD_WIN + win32con.MOD_SHIFT),
2 : (win32con.VK_F4, win32con.MOD_WIN)
}

class Modifiers(IntEnum):
    SHIFT   = win32con.MOD_SHIFT
    ALT     = win32con.MOD_ALT
    CONTROL = win32con.MOD_CONTROL
    WIN     = win32con.MOD_WIN

class GlobalHotkey:
    _hotkey_id = itertools.count(1)
    _callbacks = {}

    @staticmethod
    def register(key, modifiers, callback):
        # RegisterHotKey takes:
        #  Window handle for WM_HOTKEY messages (None = this thread)
        #  arbitrary id unique within the thread
        #  modifiers (MOD_SHIFT, MOD_ALT, MOD_CONTROL, MOD_WIN)
        #  VK code (either ord ('x') or one of win32con.VK_*)
        id = next(GlobalHotkey._hotkey_id)
        logging.info(f"Registering global hotkey [{id}] with key={key}, modifiers={modifiers}")
        registered = user32.RegisterHotKey (None, id, sum(modifiers), ord(key))
        if not registered:
            logging.error(f"Unable to register [{id}]")
            return -1
        GlobalHotkey._callbacks[id] = callback
        return id

    @staticmethod
    def listen():
        # Home-grown Windows message loop: does
        #  just enough to handle the WM_HOTKEY
        #  messages and pass everything else along.
        msg = wintypes.MSG()
        while user32.GetMessageA(byref(msg), None, 0, 0) != 0:
            if msg.message == win32con.WM_HOTKEY:
                if msg.wParam in GlobalHotkey._callbacks:
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
        logging.info(f"Unregistering global hotkey [{id}]")
        user32.UnregisterHotKey(None, id)