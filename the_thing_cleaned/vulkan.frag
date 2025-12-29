uniform sampler s;
uniform sampler sA[4];
uniform texture2D t2d;
uniform texture3D t3d[4];
int i;
uniform samplerShadow sShadow;
uniform texture3D t3d5[5];
writeonly uniform image2D i2d;
void badConst()
{
    sampler2D(t2d);
    sampler2D(s, s);
    sampler2D(i, i);
    sampler2D(t2d, i);
    sampler2D(t2d, t2d);
    sampler2D(t2d, sA);
    sampler3D[4](t3d5, sA[2]);
    sampler2D(i2d, s);
    sampler2D(t3d[1], s);
    sampler2D(t2d, sShadow);
    sampler2DShadow(t2d, s);
}
sampler2D s2D = sampler2D(t2d, s);
sampler3D s3d[4] = sampler3D[4](t3d, sA[2]);
out vec4 color;
void main()
{
    color = texture(s2D, vec2(0.5));
    color += texture(s3d[i], vec3(0.5));
}
layout(input_attachment_index = 2) uniform subpassInput subD;
layout(input_attachment_index = 3) uniform texture2D subDbad1;
layout(input_attachment_index = 4) writeonly uniform image2D subDbad2;
uniform subpassInput subDbad3;
layout(input_attachment_index = 2) uniform subpassInputMS subDMS;
void foo()
{
    vec4 v = subpassLoad(subD);
    v += subpassLoadMS(subD);
    v += subpassLoad(subD, 2);
    v += subpassLoad(subDMS, 2);
    v += subpassLoadMS(subDMS, 2);
}
subroutine int fooS;
subroutine int fooSub();
uniform vec4 dv4;
void fooTex()
{
    texture(t2d, vec2(1.0));
    imageStore(t2d, ivec2(4, 5), vec4(1.2));
}
precision highp float;
layout(location=0) in vec2 vTexCoord;
layout(location=0) out vec4 FragColor;
vec4 userTexture(mediump sampler2D samp, vec2 coord)
{
    return texture(samp, coord);
}
bool cond;
void callUserTexture()
{
    userTexture(sampler2D(t2d,s), vTexCoord);
    userTexture((sampler2D(t2d,s)), vTexCoord);
    userTexture((sampler2D(t2d,s), sampler2D(t2d,s)), vTexCoord);
    userTexture(cond ? sampler2D(t2d,s) : sampler2D(t2d,s), vTexCoord);
    gl_NumSamples;
}
void noise()
{
    noise1(dv4);
    noise2(4.0);
    noise3(vec2(3));
    noise4(dv4);
}
