#version 100
#extension GL_EXT_shader_texture_lod : require

    precision mediump float;
    varying vec2 texCoord0v;
    uniform float lod;
    uniform sampler2D tex;
    void main()
    {
        vec4 color = texture2DLodEXT(tex, texCoord0v, lod);
    }