#version 300 es
#extension GL_EXT_YUV_target : require
precision mediump float;
    yuvCscStandardEXT conv = itu_601;

    out vec4 my_color;

    void main()
    {
        vec3 yuv = rgb_2_yuv(vec3(0.0f), conv);
        vec3 rgb = yuv_2_rgb(yuv, itu_601);
        my_color = vec4(rgb, 1.0);
    }