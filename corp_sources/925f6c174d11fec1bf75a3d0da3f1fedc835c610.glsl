#version 300 es
precision mediump float;
out vec4 out_fragColor;
uniform float /* empty declarator */, uB;
void main()
{
    out_fragColor = vec4(uB, uB, uB, uB);
}
