import time


class ProgressMonitor:

    def __init__(self):
        self.started = time.time()

    def section(self, title):
        print()
        print("=" * 60)
        print(title)
        print("=" * 60)

    def start(self, name):
        print(f"[START] {name}")
        return time.time()

    def finish(self, name, started):
        elapsed = time.time() - started
        print(f"[DONE ] {name} ({elapsed:.2f}s)")
        return elapsed

    def message(self, text):
        print(f"[INFO ] {text}")

    def total(self):
        elapsed = time.time() - self.started
        print()
        print("=" * 60)
        print(f"TOTAL ELAPSED: {elapsed:.2f}s")
        print("=" * 60)
