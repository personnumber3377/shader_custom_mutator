#version 300 es
precision mediump float;
out vec4 out_fragColor;
uniform float uA, uB;
void main()
{
    vec4 color = vec4(uA, uA, uA, uB);
    out_fragColor = color;
}
