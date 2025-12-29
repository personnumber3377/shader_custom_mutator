vec3 a;
float b;
in vec4 i;
out vec4 o;
out ivec3 io;
out uvec4 uo;
flat in float fflat;
smooth in float fsmooth;
noperspective in float fnop;
uniform samplerCube sampC;
uniform sampler2D samp2D;
uniform sampler2DShadow samp2DS;
uniform sampler2DRect samp2DR;
uniform sampler2DArray samp2DA;
void bar3()
{
    o += textureGatherOffset(samp2D, vec2(0.3), ivec2(1));
    o += textureGatherOffset(samp2DA, vec3(0.3), ivec2(1));
}
void bar4()
{
    o += textureGatherOffset(samp2DR, vec2(0.3), ivec2(1));
    o += textureGatherOffset(samp2DS, vec2(0.3), 1.3, ivec2(1));
    o += textureGatherOffset(samp2D, vec2(0.3), ivec2(1), 2);
}
uniform  samplerCubeArray Sca;
uniform isamplerCubeArray Isca;
uniform usamplerCubeArray Usca;
uniform samplerCubeArrayShadow Scas;
void bar5()
{
    io = textureSize(Sca, 3);
    o += texture(Sca, i);
    io += texture(Isca, i, 0.7).xyz;
    uo = texture(Usca, i);
    o += textureLod(Sca, i, 1.7);
    a = textureSize(Scas, 3);
    float f = texture(Scas, i, i.y);
    ivec4 c = textureGrad(Isca, i, vec3(0.1), vec3(0.2));
    o += vec4(a, f + c);
}
const int ai[3] = { 10, 23, 32 };
uniform layout(binding=0) sampler2D bounds;
void bar6()
{
    mat4x3 m43;
    float a1 = m43[3].y;
    const float b = 2 * a1;
}
uniform sampler2D s2D;
uniform sampler2DRect s2DR;
uniform sampler2DRectShadow s2DRS;
uniform sampler1D s1D;
uniform sampler2DShadow s2DS;
void main()
{
    o = textureGather(sampC, vec3(0.2));
    o.y =  gl_ClipDistance[3];
    bar3();
    bar4();
    bar5();
    bar6();
}
