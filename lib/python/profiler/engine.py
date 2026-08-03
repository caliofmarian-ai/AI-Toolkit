import time


class Profiler:

    def __init__(self):
        self.timings = []
        self._incremental_stats = None

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

    def record_incremental(self, stats):
        """Store IncrementalStats so they appear in the profile summary."""
        self._incremental_stats = stats

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

        if self._incremental_stats is not None:
            s = self._incremental_stats
            print()
            print("INCREMENTAL INDEX")
            if s.cache_hit:
                print(f"  Status       cache hit")
            elif s.cache_miss:
                print(f"  Status       cache miss  (full rebuild)")
            else:
                print(f"  Status       partial rebuild")
            print(f"  Files reused {s.files_reused}")
            print(f"  Files rebuilt{s.files_rebuilt:>5}")
            print(f"  Rebuild      {s.rebuild_percentage:.1f}%")
            if s.saved_time_estimate > 0:
                print(f"  Time saved  ~{s.saved_time_estimate:.3f}s")

    def get_incremental_stats(self):
        """Return the recorded IncrementalStats or None."""
        return self._incremental_stats
