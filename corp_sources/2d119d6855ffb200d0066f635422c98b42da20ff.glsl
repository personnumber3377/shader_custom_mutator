#version 300 es
#extension GL_EXT_YUV_target : require
precision mediump float;
    yuvCscStandardEXT;
    yuvCscStandardEXT conv;
    yuvCscStandardEXT conv1 = itu_601;
    yuvCscStandardEXT conv2 = itu_601_full_range;
    yuvCscStandardEXT conv3 = itu_709;
    const yuvCscStandardEXT conv4 = itu_709;

    uniform int u;
    out vec4 my_color;

    yuvCscStandardEXT conv_standard()
    {
        switch(u)
        {
            case 1:
                return conv1;
            case 2:
                return conv2;
            case 3:
                return conv3;
            default:
                return conv;
        }
    }
    bool is_itu_601(inout yuvCscStandardEXT csc)
    {
        csc = itu_601;
        return csc == itu_601;
    }
    bool is_itu_709(yuvCscStandardEXT csc)
    {
        return csc == itu_709;
    }
    void main()
    {
        yuvCscStandardEXT conv = conv_standard();
        bool csc_check1 = is_itu_601(conv);
        bool csc_check2 = is_itu_709(itu_709);
        if (csc_check1 && csc_check2) {
            my_color = vec4(0, 1, 0, 1);
        }
    }