REQUIRED_SECTIONS = [
    "PURPOSE",
    "OBJECTIVES",
    "INPUTS",
    "OUTPUTS",
    "STATUS"
]

class Rule:

    def __init__(self, name):
        self.name = name

    def evaluate(self, document):
        raise NotImplementedError


class RequiredSectionRule(Rule):

    def __init__(self, section):
        super().__init__(section)
        self.section = section

    def evaluate(self, document):

        if document.contains(self.section):
            return True, None

        return False, f"Missing section: {self.section}"
