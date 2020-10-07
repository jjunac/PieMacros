from pathlib import Path

import yaml

from .action import Action
from .choice import *
from .logging_utils import logger

@logger
class ConfigParser:
    def __init__(self, filename):
        self.filename = filename

    def parse(self):
        config_dict = yaml.safe_load(Path(self.filename).read_text())
        self.choices = [self._parse_choice(c) for c in config_dict]
        return self

    def _parse_choice(self, choice_dict):
        if "subchoices" in choice_dict:
            return CompositeChoice(name=choice_dict["name"],
                                   subchoices=[self._parse_choice(subchoice) for subchoice in choice_dict["subchoices"]])
        return Choice(name=choice_dict["name"],
                      actions=[self._parse_action(action) for action in choice_dict["actions"]])

    def _parse_action(self, act_dict):
        if len(act_dict) != 1:
            self._logger.error(f"Ambiguous action {str(act_dict)}")
        act_type, args = next(iter(act_dict.items()))
        return Action.get_action(act_type, args)
        




