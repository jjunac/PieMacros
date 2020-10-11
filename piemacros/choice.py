
class Choice:
    def __init__(self, **kwargs):
        self.name = kwargs["name"]
        self.actions = kwargs.get("actions", None)

    def set_selector(self, selector): self.selector = selector

    def execute(self):
        self.selector.reset_choices()
        for a in self.actions:
            a.execute()


class BackChoice(Choice):
    def __init__(self):
        Choice.__init__(self, name="Back", action=None)

    def execute(self):
        self.selector.pop_choices()


class CompositeChoice(Choice):
    def __init__(self, **kwargs):
        Choice.__init__(self, **kwargs)
        self.subchoices = kwargs["subchoices"]

    def execute(self):
        self.selector.push_choices(self.subchoices)
