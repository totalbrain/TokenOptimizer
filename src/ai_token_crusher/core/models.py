from dataclasses import dataclass
from typing import Dict

@dataclass
class OptimizationResult:
    optimized_text: str
    stats: Dict[str, Dict[str, float]]
    total_saved_percent: float
    total_saved_chars: int
    total_time_ms: float
