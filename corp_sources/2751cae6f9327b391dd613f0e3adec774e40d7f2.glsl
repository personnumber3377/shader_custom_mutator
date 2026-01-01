#version 300 es
#extension GL_EXT_YUV_target : require
precision mediump float;
    yuvCscStandardEXT conv = itu_601;

    out vec4 my_color;

    void main()
    {
        lowp vec3 rgbLow = vec3(0.1);
        mediump vec3 rgbMedium = vec3(0.2);
        highp vec3 rgbHigh = vec3(0.3);

        lowp vec3 yuvLow = vec3(0.4);
        mediump vec3 yuvMedium = vec3(0.5);
        highp vec3 yuvHigh = vec3(0.6);

        my_color = vec4(
                rgb_2_yuv(rgbLow, conv) - rgb_2_yuv(rgbMedium, conv) + rgb_2_yuv(rgbHigh, conv) -
                yuv_2_rgb(yuvLow, conv) - yuv_2_rgb(yuvMedium, conv) + yuv_2_rgb(yuvHigh, conv),
            1.0);
    }