from abc import ABC, abstractmethod
import pyautogui
import time
import tkinter as tk
import tkinter.messagebox


def register_action(command):
    def decorate_action(cls):
        Action._action_types[command] = cls
        return cls
    return decorate_action


class Action(ABC):
    _action_types = {}

    @staticmethod
    def get_action(type, args):
        return Action._action_types[type](args)

    @abstractmethod
    def execute(self):
        raise NotImplementedError

@register_action("alert")
class AlertAction(Action):
    def __init__(self, args):
        self.text = " ".join(args)

    def execute(self):
        tk.messagebox.showinfo(title="PieMacros", message=self.text)

@register_action("mouse_to")
class MoveMouseAction(Action):
    def __init__(self, args):
        self.x, self.y = [int(a) for a in args.split()]

    def execute(self):
        pyautogui.moveTo(self.x, self.y)

@register_action("wait")
class WaitAction(Action):
    def __init__(self, args):
        self.timeout = float(args)

    def execute(self):
        time.sleep(self.timeout)

@register_action("hotkey")
class HotkeyAction(Action):
    def __init__(self, args):
        self.keys = args

    def execute(self):
        pyautogui.hotkey(*self.keys)

@register_action("type")
class TypeAction(Action):
    def __init__(self, args):
        self.args = args

    def execute(self):
        pyautogui.typewrite(self.args)

