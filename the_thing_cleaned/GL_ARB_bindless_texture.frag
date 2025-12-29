layout(bindless_sampler) uniform sampler2D s0;
in sampler2D s1;
uniform uvec2 s2;
uniform ivec2 s3;
uniform int index;
in sampler2D s4[2][3];
uniform BB {sampler2D s5;} bbs5[2];
in samplerBuffer s6;
uniform UBO9 {samplerBuffer s7;};
buffer SSBO10 {samplerBuffer s8;};
layout(rgba8, bindless_image) in image2D i9;
uniform vec2 coord;
uniform int icoord;
out vec4 color0;
out vec4 color1;
out vec4 color2;
out vec4 color3;
out vec4 color4;
out vec4 color5;
out vec4 color6;
out vec4 color7;
out vec4 color8;
out vec4 color9;
void main()
{
    color0 = texture(s0, coord);
    color1 = texture(s1, coord);
    color2 = texture(sampler2D(s2), coord);
    color3 = texture(sampler2D(s3), coord);
    color4 = texture(s4[index][index], coord);
    color5 = texture(bbs5[index].s5, coord);
    color6 = texelFetch(s6, icoord);
    color7 = texelFetch(s7, icoord);
    color8 = texelFetch(s8, icoord);
    color9 = imageLoad(i9, ivec2(0,0));
}
