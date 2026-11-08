"""`_Stretch` wrapper"""
__all__ = ["Stretch"]

class Stretch:
    """`_Stretch` wrapper. python-stretch library on Cython"""

    def __init__(self, channels: int, sample_rate: float):
        """:arg channels : Number of audio channels (ex. 1 for mono, 2 for stereo)
        :arg sample_rate : Audio sample rate (speed, ex. 44100)"""
        ...

    def __dealloc__(self):
        ...

    def __del__(self):
        ...

    def set_transpose_semitones(self, semitones: float):
        """Set transpose semitones"""
        ...

    def set_time_factor(self, time_factor: float):
        """Set time factor *(coefficient)*"""
        ...

    @property
    def time_factor(self):
        """Time factor *(coefficient)*"""
        ...

    @time_factor.setter
    def time_factor(self, time_factor: float):
        """Set time factor *(coefficient)*"""
        ...

    def process(self, y):
        """Process audio
        :arg y : NumPy audio data array"""
        ...
