precision highp int;
layout (location = 0) out int readSampleMaskIn;
void main () {
    readSampleMaskIn = gl_SampleMaskIn[0];
}
