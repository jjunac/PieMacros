from abc import ABC, abstractmethod
import tkinter as tk
import tkinter.messagebox
import pyautogui

class Action(ABC):
    @abstractmethod
    def execute(self):
        raise NotImplementedError

class AlertAction(Action):
    def __init__(self, args):
        self.text = args

    def execute(self):
        tk.messagebox.showinfo(title="PieMacros", message=self.text)

class MoveMouseAction(Action):
    def __init__(self, args):
        self.x, self.y = [int(a.strip()) for a in args.split(',')]

    def execute(self):
        pyautogui.moveTo(self.x, self.y)



_action_types= {
    "alert": AlertAction,
    "move mouse": MoveMouseAction,
}

def create_action(type, args):
    return _action_types[type](args)
