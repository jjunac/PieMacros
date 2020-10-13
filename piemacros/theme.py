from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
import yaml


def register_theme(name):
    def decorate_theme(cls):
        Theme._themes[name] = cls()
        return cls
    return decorate_theme


class Theme(ABC):

    @dataclass
    class Color:
        base_color: str
        accent_color: str

    _themes = {}
    _current_theme = None

    @staticmethod
    def set(name):
        Theme._current_theme = Theme._themes[name]

    @staticmethod
    def get():
        return Theme._current_theme

    @abstractmethod
    def get_choice_color(self, i, n):
        raise NotImplementedError

    @abstractmethod
    def get_back_color(self):
        raise NotImplementedError


@register_theme("rainbow")
class RainbowTheme(Theme):

    MATERIAL_COLORS = yaml.safe_load(Path("material_colors.yaml").read_text())
    SELECTOR_COLORS = ["red", "pink", "purple", "deepPurple", "indigo", "blue", "lightBlue", "cyan", "teal", "green", 
                    "lightGreen", "lime", "yellow", "amber", "orange", "deepOrange"]

    def get_choice_color(self, i, n):
        color_palette = RainbowTheme.MATERIAL_COLORS[RainbowTheme.SELECTOR_COLORS[round(len(RainbowTheme.SELECTOR_COLORS)*i/n)]]
        return Theme.Color(base_color=color_palette["400"],
                           accent_color=color_palette["A700"])

    def get_back_color(self):
        color_palette = RainbowTheme.MATERIAL_COLORS["grey"]
        return Theme.Color(base_color=color_palette["400"],
                           accent_color=color_palette["600"])


@register_theme("dark")
class DarkTheme(Theme):

    def get_choice_color(self, i, n):
        return Theme.Color(base_color="#212121",
                           accent_color="#757575")

    def get_back_color(self):
        return Theme.Color(base_color="#616161",
                           accent_color="#9e9e9e")

