lowp vec3 a;
mediump float b;
highp int c;
precision highp float;
in vec4 i;
out vec4 o;
flat in float fflat;
smooth in float fsmooth;
noperspective in float fnop;
void main()
{
    float clip = gl_ClipDistance[3];
}
uniform samplerCube sampC;
void foo()
{
    vec4 s = textureGather(sampC, vec3(0.2));
}
void bar()
{
    vec4 s = textureGather(sampC, vec3(0.2));
}
flat in vec3 gl_Color;
in vec4 gl_Color;
flat in vec4 gl_Color;
flat in vec4 gl_Color[2];
vec4 gl_Color;
void bar2()
{
    vec4 s = textureGather(sampC, vec3(0.2));
    uvec3 uv3;
    bvec3 b3;
    b3 = lessThan(uv3, uv3);
    b3 = equal(uv3, uv3);
    const bvec2 bl1 = greaterThanEqual(uvec2(2, 3), uvec2(3,3));
    const bvec2 bl2 = equal(uvec2(2, 3), uvec2(3,3));
    const bvec2 bl3 = equal(bl1, bl2);
    int a1[int(bl3.x)];
    int a2[int(bl3.y)];
    a1[0];
    a2[0];
    const bvec4 bl4 = notEqual(greaterThan(uvec4(1,2,3,4), uvec4(0,2,0,6)), lessThanEqual(uvec4(7,8,9,10), uvec4(6, 8, 0, 11)));
    int a3[int(bl4.x)+int(bl4.y)+int(bl4.z)+int(bl4.w)];
    a3[3];
    b3 != b3;
    b3 < b3;
    uv3 > uv3;
    uvec2(2, 3) >= uvec2(3,3);
    int samples = gl_NumSamples;
    int(bl4) <= int(bl4);
    int(bl4.x) > int(bl4.y);
}
uniform sampler2D samp2D;
uniform sampler2DShadow samp2DS;
uniform sampler2DRect samp2DR;
uniform sampler2DArray samp2DA;
void bar23()
{
    vec4 s;
    s = textureGatherOffset(sampC, vec3(0.3), ivec2(1));
    s = textureGatherOffset(samp2DR, vec2(0.3), ivec2(1));
    s = textureGatherOffset(samp2D, vec2(0.3), ivec2(1));
    s = textureGatherOffset(samp2DA, vec3(0.3), ivec2(1));
    s = textureGatherOffset(samp2DS, vec2(0.3), 1.3, ivec2(1));
    s = textureGatherOffset(samp2D, vec2(0.3), ivec2(1), 2);
    int samples = gl_NumSamples;
}
void bar234()
{
    vec4 s;
    s = textureGatherOffset(samp2D, vec2(0.3), ivec2(1));
    s = textureGatherOffset(samp2DA, vec3(0.3), ivec2(1));
    s = textureGatherOffset(samp2DR, vec2(0.3), ivec2(1));
    s = textureGatherOffset(samp2DS, vec2(0.3), 1.3, ivec2(1));
    s = textureGatherOffset(samp2D, vec2(0.3), ivec2(1), 2);
}
uniform  samplerCubeArray Sca;
uniform isamplerCubeArray Isca;
uniform usamplerCubeArray Usca;
uniform samplerCubeArrayShadow Scas;
void bar235()
{
    ivec3 a = textureSize(Sca, 3);
    vec4 b = texture(Sca, i);
    ivec4 c = texture(Isca, i, 0.7);
    uvec4 d = texture(Usca, i);
    b = textureLod(Sca, i, 1.7);
    a = textureSize(Scas, a.x);
    float f = texture(Scas, i, b.y);
    c = textureGrad(Isca, i, vec3(0.1), vec3(0.2));
}
int \
    x;
const int ai[3] = { 10, 23, 32 };
layout(binding=0) uniform blockname { int a; } instanceName;
uniform layout(binding=0) sampler2D bounds;
void bar23444()
{
    mat4x3 m43;  \
    float a1 = m43[3].y;
    vec3 v3;
    int a2 = m43.length();
    a2 += m43[1].length();
    a2 += v3.length();
    const float b = 2 * a1;
    a.x = gl_MinProgramTexelOffset + gl_MaxProgramTexelOffset;
    bool boolb;
    boolb.length();
    m43[3][1].length();
    v3.length;
    v3.length(b);
}
in float gl_FogFragCoord;
in float gl_FogFragCoord;
in int gl_FogFragCoord;
layout(r32i) uniform iimage2D iimg2Dbad;
layout(r32i) uniform iimage2D iimg2D;
void qux2()
{
    int i;
    imageAtomicCompSwap(iimg2D, ivec2(i,i), i, i);
    ivec4 pos = imageLoad(iimg2D, ivec2(i,i));
}
layout(location = 3) uniform vec4 ucolor0;
layout(location = 4) uniform vec4 ucolor1;
