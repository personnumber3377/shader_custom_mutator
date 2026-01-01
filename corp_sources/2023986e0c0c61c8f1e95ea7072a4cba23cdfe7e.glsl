#version 100
#extension GL_EXT_blend_func_extended : require
#extension GL_EXT_draw_buffers : require
precision mediump float;
void main() {
    gl_FragData[gl_MaxDrawBuffers - 1] = vec4(1.0);
    gl_SecondaryFragDataEXT[gl_MaxDualSourceDrawBuffersEXT - 1] = vec4(0.1);
}
