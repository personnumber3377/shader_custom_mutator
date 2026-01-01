#version 300 es
#extension GL_EXT_YUV_target : require
precision mediump float;
    yuvCscStandardEXT conv = itu_709;

    out vec4 my_color;

    vec3 f(vec3 v) { return v + vec3(0.1); }

    void main()
    {
        vec3 rgb = yuv_2_rgb(f(rgb_2_yuv(vec3(0.0f), conv)), conv);
        my_color = vec4(rgb, 1.0);
    }