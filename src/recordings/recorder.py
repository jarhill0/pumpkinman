from io import BytesIO
from typing import Callable, Dict, Optional

from .formats import BaseRecordingFormat, Recording001


class Recorder:
    @property
    def recording(self) -> bool:
        return bool(self._recording)

    def __init__(self):
        self._bytes: Optional[BytesIO] = None
        self._recording: Optional[BaseRecordingFormat] = None
        self._callback: Optional[Callable[[Dict[str, bool]], None]] = None

    def take(self, change: [Dict[str, bool]]):
        if self.recording:
            self._callback(change)

    def start(self):
        self._bytes = BytesIO()
        self._recording = Recording001(self._bytes)
        self._callback = self._recording.start_recording()

    def stop(self) -> bytes:
        self._recording.stop_and_save_recording()
        result = self._bytes.getvalue()
        self._bytes.close()

        self._recording = None
        self._bytes = None
        self._callback = None

        return result
