#version 300 es
precision mediump float;
    float rgb_2_yuv(float x) { return x + 1.0; }

    in float i;
    out float o;

    void main()
    {
        o = rgb_2_yuv(i);
    }