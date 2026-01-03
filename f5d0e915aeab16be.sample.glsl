HEADER: frag 2 2
#version 300 es
precision mediump float;
out vec4 out_fragColor;
uniform float uB;
void main()
{
    out_fragColor = vec4(uB, uB, uB, uB);
}
