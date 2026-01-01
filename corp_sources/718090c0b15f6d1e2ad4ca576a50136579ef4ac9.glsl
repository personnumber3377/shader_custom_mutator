#version 100
#extension GL_EXT_shadow_samplers : require

    precision mediump float;
    varying vec3 texCoord0v;
    uniform sampler2DShadow tex;
    void main()
    {
        float color = shadow2DEXT(tex, texCoord0v);
    }