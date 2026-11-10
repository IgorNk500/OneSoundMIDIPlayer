"""Fast sound sampler class, based on custom audio daemon (thread)"""
from typing import Optional
__all__ = ["Sampler"]

class Sampler:
    """Fast one sound sampler"""
    @property
    def is_playing(self) -> bool:
        """Audio daemon status"""

    @property
    def buffer_size(self) -> int:
        """Sampler buffer size
        :returns : Buffer size"""

    @property
    def root_note(self) -> int:
        """Sample base note
        :returns : Root note number *(in MIDI format)*"""

    @property
    def root_key(self) -> int:
        """Sample base note
        :returns : Root note number *(in MIDI format)*"""

    @property
    def num_channels(self) -> int:
        """Sample channels number (ex. 1 for mono, 2 for stereo)"""

    @property
    def sr(self) -> int:
        """Sound samplerate"""

    # Alias
    @property
    def samplerate(self) -> int:
        """Sound samplerate"""


    def __init__(self, sample_path: str, root_note: int = 60, buffer_size: Optional[int] = None):
        """Init sampler
        :arg sample_path : Path to sample sound file
        :arg root_note   : Sample base note
        :arg buffer_size : Sampler buffer size; Set to None or 0 for auto sizing
        """

    def note_on(self, note: int = 60, velocity: float = 1.0,
                time_factor: float = 1.0, loop: bool = False):
        """Enable one note
        :arg note        : Note number *(in MIDI format)*
        :arg velocity    : Out velocity *(volume)*
        :arg time_factor : Speed modifier
        :arg loop        : `True` - the sound repeats; `False` - the sound not repeats
        """

    def note_off(self, note: int = 60):
        """Disable one note. If note not enabled, calls logger error *(not exception)*
        :arg note : Note number *(in MIDI format)*"""

    def safe_note_off(self, note: int = 60) -> bool:
        """Disable one note. If note not enabled, do nothing
        :arg note : Note number *(in MIDI format)*
        :returns  : `True` - note disabled successfully; `False` - note not enabled"""

    def playing(self, note: int = 60) -> bool:
        """Note status
        :arg note : Note number *(in MIDI format)*
        :returns  : `True` - note enabled; `False` - note disabled"""

    def restart(self):
        """Restart audio daemon (thread) if it's stopped"""

    def close(self):
        """Stop audio daemon"""
