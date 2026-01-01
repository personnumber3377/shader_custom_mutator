#version 300 es
precision mediump float;
    float yuv_2_rgb(float x) { return x + 1.0; }

    in float i;
    out float o;

    void main()
    {
        o = yuv_2_rgb(i);
    }