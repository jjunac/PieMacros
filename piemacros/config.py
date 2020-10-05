from pathlib import Path

import yaml

from . import action
from  .choice import *

class ConfigParser:
    def __init__(self, filename):
        self.filename = filename

    def parse(self):
        config_dict = yaml.safe_load(Path(self.filename).read_text())
        self.choices = [self._parse_choice(c) for c in config_dict]
        return self

    def _parse_choice(self, choice_dict):
        if "subchoices" in choice_dict:
            return CompositeChoice(name=choice_dict["name"], subchoices=[self._parse_choice(subchoice) for subchoice in choice_dict["subchoices"]])
        return Choice(name=choice_dict["name"], action=self._parse_action(choice_dict["action"]))

    def _parse_action(self, act_str):
        act_argv = act_str.split(" ")
        return action.create_action(act_argv[0], act_argv[1:])
        




