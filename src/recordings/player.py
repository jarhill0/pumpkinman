from io import BytesIO
from typing import Awaitable, Callable, Dict, Optional, Type

from .formats import BaseRecordingFormat, Recording001


class Player:
    KNOWN_VERSIONS = {
        1: Recording001,
    }

    def _recording_kind(self) -> Type[BaseRecordingFormat]:
        version = BaseRecordingFormat.version(self._bytes)
        kind = Player.KNOWN_VERSIONS.get(version)
        if kind:
            return kind
        raise Exception('Unknown version number!')

    def __init__(self, file, send: Callable[[Dict[str, bool]], Awaitable[None]]):
        self._bytes: BytesIO = BytesIO()
        file.save(self._bytes)
        self._recording: BaseRecordingFormat = self._recording_kind()(self._bytes)
        self._send: Optional[Callable[[Dict[str, bool]], Awaitable[None]]] = send

    async def play(self):
        await self._recording.play(self._send)

    def stop(self):
        self._recording.stop_playing()
