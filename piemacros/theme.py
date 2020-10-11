from dataclasses import dataclass
from pathlib import Path
import yaml


class Theme:

    @dataclass
    class Color:
        base_color: str
        accent_color: str


    MATERIAL_COLORS = yaml.safe_load(Path("material_colors.yaml").read_text())
    SELECTOR_COLORS = ["red", "pink", "purple", "deepPurple", "indigo", "blue", "lightBlue", "cyan", "teal", "green", 
                    "lightGreen", "lime", "yellow", "amber", "orange", "deepOrange"]

    @staticmethod
    def get_choice_color(i, n):
        color_palette = Theme.MATERIAL_COLORS[Theme.SELECTOR_COLORS[round(len(Theme.SELECTOR_COLORS)*i/n)]]
        return Theme.Color(base_color=color_palette["400"],
                           accent_color=color_palette["A700"])

    @staticmethod
    def get_back_color():
        color_palette = Theme.MATERIAL_COLORS["grey"]
        return Theme.Color(base_color=color_palette["400"],
                           accent_color=color_palette["600"])

