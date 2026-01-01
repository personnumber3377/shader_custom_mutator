#extension GL_EXT_blend_func_extended : require
precision mediump float;
void main() { gl_FragColor = vec4(gl_MaxDualSourceDrawBuffersEXT / 10); }
