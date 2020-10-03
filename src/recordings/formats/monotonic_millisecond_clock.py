import time


class MonotonicMillisecondClock:
    """A monotonic class that reports time in integer milliseconds."""

    @staticmethod
    def _monotonic_ms() -> int:
        return time.monotonic_ns() // 1000000

    def __init__(self):
        self.zero: int = 0
        self.mark()

    def mark(self) -> None:
        """Mark the zero point for the clock."""
        self.zero = self._monotonic_ms()

    def now(self):
        return self._monotonic_ms() - self.zero
