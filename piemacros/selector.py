from functools import wraps

from .choice import BackChoice, Choice
from .logging_utils import logger

@logger
class Selector:
    def __init__(self, choices):
        self._base_choices = choices
        for c in self._base_choices:
            c.set_selector(self)
        self._back_choice = BackChoice()
        self._back_choice.set_selector(self)
        self._choice_stack = []
        self._observers = set()

    def notify(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            res = func(*args, **kwargs)
            for o in args[0]._observers:
                o.on_selector_update()
            return res
        return wrapper

    def get_current_choices(self):
        return self._choice_stack[-1] if self._choice_stack else None

    def get_back_choice(self): return self._back_choice

    def subscribe(self, observer): self._observers.add(observer)

    def unsubscribe(self, observer): self._observers.remove(observer)

    @notify
    def reset_choices(self):
        if self._choice_stack:
            self._base_choices = self._choice_stack[0]
            self._choice_stack.clear()

    @notify
    def pop_choices(self):
        self._choice_stack.pop()

    @notify
    def push_choices(self, choices):
        self._choice_stack.append(choices)
        for c in self._choice_stack[-1]:
            c.set_selector(self)

    @notify
    def init_choices(self):
        self._choice_stack = [self._base_choices]


