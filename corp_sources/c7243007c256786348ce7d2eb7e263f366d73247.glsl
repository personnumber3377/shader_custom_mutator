#version 300 es
#extension GL_EXT_YUV_target : require
precision mediump float;
    uniform __samplerExternal2DY2YEXT uSampler;
    layout(yuv) out vec4 fragColor;
    void main() {
        fragColor = vec4(texture(uSampler, vec2(0.0)).zyx, 1.0);
    }