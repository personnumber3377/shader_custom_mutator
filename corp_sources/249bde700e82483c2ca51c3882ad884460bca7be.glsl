#version 300 es
#extension GL_EXT_clip_cull_distance : require

    out highp vec4 fragColor;

    void main()
    {
        fragColor = vec4(gl_ClipDistance[0], gl_CullDistance[0], 0, 1);
    }