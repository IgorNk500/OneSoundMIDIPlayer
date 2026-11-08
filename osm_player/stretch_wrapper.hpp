// stretch_wrapper.hpp
// Fast access to Signalsmith Stretch from Cython
#pragma once
#include <signalsmith-stretch.h>

using StretchFloat = signalsmith::stretch::SignalsmithStretch<float>;

extern "C" {
    StretchFloat* stretch_create();
    void stretch_destroy(StretchFloat* self);
    void stretch_preset(StretchFloat* self, int channels, float sample_rate);
    void stretch_set_transpose_semitones(StretchFloat* self, float semitones);
    void stretch_process(StretchFloat* self, float** input, int input_samples, float** output, int output_samples);
}