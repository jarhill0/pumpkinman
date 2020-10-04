from typing import Awaitable, BinaryIO, Callable, Dict


class BaseRecordingFormat:
    """Base for all recording file formats."""

    HEADER = b'JrhPumpRec'

    @staticmethod
    def version(file: BinaryIO) -> int:
        """
        Get the format version of the open file.
        :param file: An open and readable binary file object
        :return: The version number
        """
        file.seek(0)
        header = file.read(10)
        if header != BaseRecordingFormat.HEADER:
            raise ValueError('Not a pumpkin man recording!')
        version_byte = file.read(1)
        if version_byte:
            return version_byte[0]
        raise ValueError('No version in header!')

    def __init__(self, file: BinaryIO):
        """
        Initialize the format.

        :param file: An open binary file object, readable or writable as necessary to play/record.
        """
        self.file = file

    async def play(self, send: Callable[[Dict[str, bool]], Awaitable[None]]) -> None:
        """
        Play this file.

        :param send: A callback that takes the same type of dict passed into start_recording and takes action.
        """
        raise NotImplementedError()

    def stop_playing(self):
        """Stop playing this file."""
        raise NotImplementedError()

    def start_recording(self) -> Callable[[Dict[str, bool]], None]:
        """
        Start recording to this file.

        :return: A callback that takes a dict of {'output_name': True/False, ...} at the moment that change takes effect
        """
        raise NotImplementedError()

    def stop_and_save_recording(self) -> None:
        """Stop recording and save to the file."""
        raise NotImplementedError()
