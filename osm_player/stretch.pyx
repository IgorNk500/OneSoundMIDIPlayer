# cython: language_level=3
# _Stretch.pyx wrapper
cimport numpy as cnp
cnp.import_array()

from . cimport _stretch
from ._stretch import Stretch as _Stretch

class Stretch:
    def __init__(self, channels: int, sample_rate: float):
        self._instance = _Stretch()
        self._instance.preset(channels, sample_rate)

    def __dealloc__(self): self._instance.__dealloc__()
    def __del__(self): self._instance.__dealloc__()


    def set_transpose_semitones(self, semitones: float):
        self._instance.setTransposeSemitones(semitones)

    def set_time_factor(self, time_factor: float):
        self._instance.setTimeFactor(time_factor)

    @property
    def time_factor(self): return self._instance.time_factor

    @time_factor.setter
    def time_factor(self, time_factor: float): self._instance.setTimeFactor(time_factor)

    def process(self, y):
        self._instance.process(
            <cnp.ndarray[cnp.float32_t, ndim=2, mode="c"]>y
        )
