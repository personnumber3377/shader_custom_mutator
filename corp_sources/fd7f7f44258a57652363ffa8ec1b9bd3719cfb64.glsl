#version 100
#extension GL_EXT_frag_depth : require

    precision mediump float;

    void main()
    {
        gl_FragDepthEXT = 1.0;
    }