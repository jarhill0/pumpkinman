from asyncio import sleep
from json import dumps, loads
from typing import Awaitable, BinaryIO, Callable, Dict, List, Optional

from .base import BaseRecordingFormat
from .monotonic_millisecond_clock import MonotonicMillisecondClock


class Recording001(BaseRecordingFormat):
    """Version 1 of recording format."""

    MAX_TIME = 2 ** 32
    VERSION = 1
    SLEEP_AMOUNT = 1/30

    def __init__(self, file: BinaryIO):
        """
        Initialize the format.

        :param file: An open binary file object, readable or writable as necessary to play/record.
        """
        super().__init__(file)
        self.playing: bool = False
        self.recording: bool = False
        self.stopped: bool = False
        self.data: Optional[List] = None
        self.clock = MonotonicMillisecondClock()

    def _check_header_and_version(self):
        version = BaseRecordingFormat.version(self.file)
        if version != Recording001.VERSION:
            raise ValueError(f'Expected version {Recording001.VERSION} but found version {version}!')

    async def play(self, send: Callable[[Dict[str, bool]], Awaitable[None]]) -> None:
        """"
        Play this file.

        :param send: A callback that takes the same type of dict passed into start_recording and takes action.
        """
        self._check_header_and_version()
        raw_json = str(self.file.read(), 'ascii')
        self.data = loads(raw_json)

        self.clock.mark()
        for time, change in self.data:
            while time > self.clock.now():
                await sleep(Recording001.SLEEP_AMOUNT)

            await send(change)

    def start_recording(self) -> Callable[[Dict[str, bool]], None]:
        """
        Start recording to this file.

        :return: A callback that takes a dict of {'output_name': True/False, ...} at the moment that change takes effect
        """
        if self.playing:
            raise ValueError('Already playing!')
        if self.recording:
            raise ValueError('Already recording!')
        self.recording = True
        self.data = []

        def callback(change: Dict[str, bool]) -> None:
            self.data.append([self.clock.now(), change])

        self.clock.mark()
        return callback

    def stop_and_save_recording(self) -> None:
        """Stop recording and save to the file."""
        if not self.recording or self.stopped:
            raise ValueError('Not recording, or recording already stopped.')
        self.stopped = True

        self.data.sort(key=lambda item: item[0])

        self.file.seek(0)
        self.file.write(BaseRecordingFormat.HEADER)
        self.file.write(bytes([Recording001.VERSION]))
        json_bytes = bytes(dumps(self.data), 'ascii')
        self.file.write(json_bytes)
