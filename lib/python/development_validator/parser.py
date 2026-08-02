from pathlib import Path

class DevelopmentDocument:

    def __init__(self, path):
        self.path = Path(path)
        self.text = self.path.read_text(encoding="utf-8")
        self.lines = self.text.splitlines()

    def contains(self, value):
        return value in self.text
