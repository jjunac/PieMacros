# import ctypes
import win32process
import win32con
import win32api
import win32gui
import psutil

from pywinauto.application import Application, ProcessNotFoundError


# def callback(hwnd, _):
#     tid, pid = win32process.GetWindowThreadProcessId(hwnd)
#     active_window_path = psutil.Process(pid).exe()


#     print(active_window_path)


# win32gui.EnumWindows(callback, None)



# app = Application(backend="uia").start('notepad.exe')

def open_or_focus(exe):
    try:
        app = Application(backend="uia").connect(title_re=".*Mozilla Firefox", found_index=0)
        print(app.windows())
        app.windows()[0].set_focus()
    except ProcessNotFoundError:
        app = Application(backend="uia").start(exe)


open_or_focus("firefox.exe")


