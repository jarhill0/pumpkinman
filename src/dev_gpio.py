"""Mocks for the Raspberry Pi GPIO library, for use in development."""

from typing import Any, Iterable, Union

BCM = 'BCM'
LOW = False
HIGH = True


def setmode(mode: Any):
    print(f'Mode set to {mode}.')


def output(pins: Union[Iterable[int], int], values: Union[Iterable[bool], bool]):
    if isinstance(pins, int):
        print(f'Pin {pins} set to {values}')
    else:
        for pin, value in zip(pins, values):
            output(pin, value)

def cleanup():
    print('Cleaning up.')