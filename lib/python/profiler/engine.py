import time


class Profiler:

    def __init__(self):
        self.timings = []

    def run(self, name, fn):

        print(f"[ENGINE] {name} ...", flush=True)

        started = time.perf_counter()

        result = fn()

        elapsed = time.perf_counter() - started

        self.timings.append({
            "engine": name,
            "elapsed": elapsed,
        })

        print(
            f"[DONE  ] {name} ({elapsed:.2f}s)",
            flush=True
        )

        return result

    def summary(self):

        print()
        print("=" * 60)
        print("ENGINE PROFILE")
        print("=" * 60)

        total = 0.0

        for item in self.timings:

            total += item["elapsed"]

            print(
                f'{item["engine"]:<30} {item["elapsed"]:>8.2f}s'
            )

        print("-" * 60)
        print(f"TOTAL{'':24}{total:>8.2f}s")
