void main()
{
}
uniform float f;
layout(location = 2) uniform float g;
uniform sampler2D s1;
layout(location = 3) uniform sampler2D s2;
void noise()
{
    noise1(vec4(1));
    noise2(4.0);
    noise3(vec2(3));
    noise4(1);
}
uniform atomic_uint atomic;
layout(input_attachment_index = 1) uniform subpassInput sub;
