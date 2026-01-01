#version 300 es
#extension GL_EXT_blend_func_extended : require
precision mediump float;
layout(location = 0) out mediump vec4 fragColor;void main() {
    fragColor = vec4(gl_MaxDualSourceDrawBuffersEXT / 10);
}
