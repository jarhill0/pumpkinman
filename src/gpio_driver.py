from sys import stderr
from typing import Dict, Iterable, Tuple

try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:
    print('Cannot load RPi.GPIO library. Using development stubs.', file=stderr)
    import dev_gpio as GPIO


class GPIODriver:
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

    def clear(self):
        """Set all pins to low."""
        self.bulk_set({pin: GPIO.LOW for pin in self.all_pins})

    def set(self, pin: int, value: bool):
        """
        Set a single pin.

        :param pin: The pin index.
        :param value: The value to set.
        """
        GPIO.output(self._raw_pin_number(pin), value)

    __setitem__ = set

    def bulk_set(self, settings: Dict[int, bool]):
        """
        Set pins to values.

        :param settings: A dict mapping pin indices to pin states .
        """
        pins = []
        values = []
        for pin, value in settings.items():
            pins.append(self._raw_pin_number(pin))
            values.append(value)
        GPIO.output(pins, values)

    def _raw_pin_number(self, pin: int):
        return self.pin_numbers[pin]
