int a[3] = { 2, 3, 4, };
int uint;
attribute vec4 v[3];
float f = 2;
uniform block {
    int x;
};
void foo(float);
void main()
{
    foo(3);
    int s = 1 << 4;
    s = 16 >> 2;
    if (a == a);
    int b, c;
    b = c & 4;
    b = c % 4;
    b = c | 4;
    b >>= 2;
    b <<= 2;
    b %= 3;
    struct S {
        float f;
        float a[10];
    } s1, s2;
    s1 = s2;
    if (s1 == s2);
    if (s1 != s2);
    switch(b) {
    }
}
invariant gl_FragColor;
float fa[];
float f13;
invariant f13;
struct S { int a; };
invariant S;
invariant float fi;
varying vec4 av;
invariant av;
void foo10()
{
    invariant f;
    invariant float f2;
    float f3;
    invariant f3;
}
uniform vec2 uv2;
invariant uv2;
invariant uniform vec3 uv3;
sampler2D glob2D;
void f11(sampler2D p2d)
{
    sampler2D v2D;
}
varying sampler2D vary2D;
struct sp {
    highp float f;
    in float g;
    uniform float h;
    invariant float i;
};
uniform sampler3D s3D;
precision highp sampler3D;
uniform sampler3D s3D2;
void foo234()
{
    texture3D(s3D2, vec3(0.2), 0.2);
    texture3DProj(s3D2, v[1], 0.4);
    dFdx(v[0]);
    dFdy(3.2);
    fwidth(f13);
}
void foo236()
{
    dFdx(v[0]);
    dFdy(3.2);
    fwidth(f13);
    gl_FragDepth = f13;
    gl_FragDepthEXT = f13;
}
void foo239()
{
    gl_FragDepth = f13;
    gl_FragDepthEXT = f13;
}
uniform samplerExternalOES sExt;
void foo245()
{
    texture2D(sExt, vec2(0.2));
    texture2DProj(sExt, vec3(f13));
    texture2DProj(sExt, v[2]);
}
precision mediump samplerExternalOES;
uniform samplerExternalOES mediumExt;
uniform highp samplerExternalOES highExt;
void foo246()
{
    texture2D(mediumExt, vec2(0.2));
    texture2DProj(highExt, v[2]);
    texture3D(sExt, vec3(f13));
    texture2DProjLod(sExt, vec3(f13), f13);
    int a;
    ~a;
    a | a;
    a & a;
}
uniform sampler2D s2Dg;
int foo203940(int a, float b, float a)
{
    texture2DProjGradEXT(s2Dg, vec3(f13), uv2, uv2);
    return a;
}
float f123 = 4.0f;
float f124 = 5e10F;
uniform samplerCube sCube;
void foo323433()
{
    texture2DLodEXT(s2Dg, uv2, f13);
    texture2DProjGradEXT(s2Dg, vec3(f13), uv2, uv2);
    texture2DGradEXT(s2Dg, uv2, uv2, uv2);
    textureCubeGradEXT(sCube, vec3(f13), vec3(f13), vec3(f13));
}
int fgfg(float f, mediump int i);
int fgfg(float f, highp int i) { return 2; }
int fffg(float f);
int fffg(float f);
int gggf(float f);
int gggf(float f) { return 2; }
int agggf(float f) { return 2; }
int agggf(float f);
int agggf(float f);
varying struct SSS { float f; } s;
int vf(void);
int vf2();
int vf3(void v);
int vf4(int, void);
int vf5(int, void v);
void badswizzle()
{
    vec3 a[5];
    a.y;
    a.zy;
    a.nothing;
    a.length();
    a.method();
}
float fooinit();
float fooinittest()
{
    return fooinit();
}
void blendFuncFail()
{
    gl_SecondaryFragColorEXT = vec4(1.0);
    gl_SecondaryFragDataEXT[gl_MaxDualSourceDrawBuffersEXT - 1] = vec4(0.1);
}
void blendFunc()
{
    gl_SecondaryFragColorEXT = vec4(1.0);
    gl_SecondaryFragDataEXT[gl_MaxDualSourceDrawBuffersEXT - 1] = vec4(0.1);
}
const float fi1 = 3.0;
const float fi2 = 4.0;
const float fi3 = 5.0;
float fooinit()
{
    return fi1 + fi2 + fi3;
}
int init1 = gl_FrontFacing ? 1 : 2;
int init2 = gl_FrontFacing ? 1 : 2;
int a__b;
uniform samplerExternalOES badExt;
