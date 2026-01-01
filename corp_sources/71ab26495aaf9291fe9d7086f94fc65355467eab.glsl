#version 300 es
#extension GL_EXT_YUV_target : require
precision mediump float;
    yuvCscStandardEXT conv = itu_601_full_range;

    out vec4 my_color;

    void main()
    {
        vec3 rgb = yuv_2_rgb(vec3(0.1) + rgb_2_yuv(vec3(0.0f), conv), conv);
        my_color = vec4(rgb, 1.0);
    }