from sys import stderr
from typing import Dict, Iterable, Tuple

try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:
    print("Cannot load RPi.GPIO library. Using development stubs.", file=stderr)
    from . import dev_gpio as GPIO


class RelayDriver:
    """Drive a relay board with a simple interface."""

    @staticmethod
    def stop():
        """Stop and clean up."""
        GPIO.cleanup()

    def __init__(self, pin_numbers: Iterable[int] = (2, 3, 4, 17, 27, 22, 10, 9)):
        """
        Initialize the driver.

        :param pin_numbers: a tuple of GPIO pin numbers in the order you wish to address them (starting with 0).
        """
        self.pin_numbers: Tuple[int] = tuple(pin_numbers)
        self.pin_count: int = len(self.pin_numbers)
        self.all_pins: Tuple[int] = tuple(range(self.pin_count))
        GPIO.setmode(GPIO.BCM)
        for pin in self.pin_numbers:
            GPIO.setup(pin, GPIO.OUT)

    def clear(self):
        """Disable all relays."""
        self.bulk_set({pin: False for pin in self.all_pins})

    def set(self, relay: int, value: bool):
        """
        Set a single relay.

        :param relay: The relay index.
        :param value: The value to set.
        """
        GPIO.output(self._pin_number(relay), self._coerce_value(value))

    __setitem__ = set

    def bulk_set(self, settings: Dict[int, bool]):
        """
        Set relays to values.

        :param settings: A dict mapping relay indices to relay states.
        """
        pins = []
        values = []
        for pin, value in settings.items():
            pins.append(self._pin_number(pin))
            values.append(self._coerce_value(value))
        GPIO.output(pins, values)

    @staticmethod
    def _coerce_value(value):
        return GPIO.LOW if value else GPIO.HIGH

    def _pin_number(self, pin: int):
        return self.pin_numbers[pin]
