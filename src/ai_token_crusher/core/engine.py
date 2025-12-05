import time
from typing import Dict, Callable
from .models import OptimizationResult
from .config import OPTIONS_DEFAULT

class OptimizationEngine:
    def __init__(self):
        self.techniques: Dict[str, Callable[[str], str]] = {}
        self.order = list(OPTIONS_DEFAULT.keys())

    def register(self, name: str, func: Callable[[str], str]):
        self.techniques[name] = func
        if name not in self.order:
            self.order.append(name)

    def apply(self, text: str, options: Dict[str, bool]) -> OptimizationResult:
        start = time.perf_counter()
        result = text
        stats = {}

        for name in self.order:
            if options.get(name, False) and name in self.techniques:
                func = self.techniques[name]
                t0 = time.perf_counter()
                before = len(result)
                result = func(result)
                after = len(result)
                t = (time.perf_counter() - t0) * 1000

                saved = before - after
                pct = saved / before * 100 if before else 0
                stats[name] = {"time_ms": t, "saved_chars": saved, "saved_percent": pct}

        total_time = (time.perf_counter() - start) * 1000
        total_saved = len(text) - len(result)
        total_pct = total_saved / len(text) * 100 if text else 0
        stats["TOTAL"] = {"time_ms": total_time, "saved_percent": total_pct, "saved_chars": total_saved}

        return OptimizationResult(
            optimized_text=result.rstrip() + ("\n" if result.strip() else ""),
            stats=stats,
            total_saved_percent=total_pct,
            total_saved_chars=total_saved,
            total_time_ms=total_time,
        )
