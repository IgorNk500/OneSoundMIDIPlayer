# _Stretch.pyx class definition
cimport numpy as cnp

cdef extern from "stretch_wrapper.hpp":
    ctypedef struct StretchFloat:
        pass

    StretchFloat* stretch_create() nogil
    void stretch_destroy(StretchFloat*) nogil
    void stretch_preset(StretchFloat*, int channels, float sample_rate) nogil
    void stretch_set_transpose_semitones(StretchFloat*, float semitones) nogil
    void stretch_set_time_factor(StretchFloat*, float time_factor) nogil
    void stretch_process(StretchFloat*, float** input, int input_samples, float** output, int output_samples) nogil

cdef class Stretch:
    cdef StretchFloat* _instance
    cdef float _time_factor

    cpdef void preset(self, int channels, float sample_rate)
    cpdef void setTransposeSemitones(self, float semitones)
    cpdef void setTimeFactor(self, float time_factor)
    cpdef cnp.ndarray[cnp.float32_t, ndim=2, mode="c"] process(self, cnp.ndarray[cnp.float32_t, ndim=2, mode="c"] y)