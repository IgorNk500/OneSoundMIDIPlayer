# distutils: sources = src/stretch_wrapper.cpp
# cython: boundscheck=False
"""python-stretch library on Cython"""

import numpy as np
cimport numpy as cnp

from libc.stdlib cimport malloc, free

# Init NumPy API
cnp.import_array()

cdef class Stretch:
    """Cython Signalsmith Strech wrapper"""
    def __cinit__(self):
        self._instance = stretch_create()
        self._time_factor = 1.0

    def __dealloc__(self):
        if self._instance != NULL:
            stretch_destroy(self._instance)

    cpdef void preset(self, int channels, float sample_rate):
        stretch_preset(self._instance, channels, sample_rate)

    cpdef void setTransposeSemitones(self, float semitones):
        stretch_set_transpose_semitones(self._instance, semitones)

    cpdef void setTimeFactor(self, float time_factor):
        self._time_factor = time_factor

    @property
    def time_factor(self): return self._time_factor

    @time_factor.setter
    def time_factor(self, float time_factor): self.setTimeFactor(time_factor)

    cpdef cnp.ndarray[cnp.float32_t, ndim=2, mode="c"] process(self, cnp.ndarray[cnp.float32_t, ndim=2, mode="c"] y):
        # data format: (channels, samples)
        #cdef cnp.ndarray[cnp.float32_t, ndim=2, mode="c"] output
        cdef StretchFloat* instance = self._instance
        cdef float ** input_ptrs
        cdef float ** output_ptrs

        cdef int i

        cdef int n_channels = y.shape[0]
        cdef int input_samples = y.shape[1]
        cdef int output_samples = <int>(input_samples * self._time_factor)

        #cdef cnp.ndarray[cnp.float32_t, ndim=2, mode="c"] output = np.zeros((n_channels, output_samples), dtype=np.float32)
        cdef cnp.ndarray[cnp.float32_t, ndim=2, mode="c"] output = np.zeros((n_channels, output_samples), dtype=np.float32)

        with nogil:
            input_ptrs  = <float**>malloc(n_channels * sizeof(float*))
            output_ptrs = <float**>malloc(n_channels * sizeof(float*))

            for i in range(n_channels):
                input_ptrs[i]  = &y[i, 0]
                output_ptrs[i] = &output[i, 0]

            stretch_process(instance, input_ptrs, input_samples, output_ptrs, output_samples)

            # Free buffers
            free(input_ptrs)
            free(output_ptrs)
        return output
