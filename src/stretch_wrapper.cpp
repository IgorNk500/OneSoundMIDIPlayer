// stretch_wrapper.cpp
// Fast access to Signalsmith Stretch from Cython
#include <stretch_wrapper.hpp>

StretchFloat* stretch_create() {
    return new StretchFloat();
}
void stretch_destroy(StretchFloat* self) { delete self; }

void stretch_preset(StretchFloat* self, int channels, float sample_rate) {
    self->presetDefault(channels, sample_rate);
}

void stretch_set_transpose_semitones(StretchFloat* self, float semitones) {
    self->setTransposeSemitones(semitones);
}

void stretch_process(StretchFloat* self, float** input, int input_samples, float** output, int output_samples) {
    self->process(input, input_samples, output, output_samples);
}
