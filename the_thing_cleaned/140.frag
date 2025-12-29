varying vec4 v;
in vec4 i;
out vec4 o;
in float gl_ClipDistance[5];
void main()
{
    float clip = gl_ClipDistance[2];
}
in struct S { float f; } s;
float patch = 3.1;
layout(location=3) in vec4 vl;
layout(location = 3) out vec4 factorBad;
layout(location = 5) out vec4 factor;
layout(location=4) in vec4 vl2;
float fooi();
void foo()
{
    vec2 r1 = modf(v.xy, v.zw);
    vec2 r2 = modf(o.xy, o.zw);
    o.z = fooi();
}
float i1 = gl_FrontFacing ? -2.0 : 2.0;
float i2 = 102;
float fooi()
{
    return i1 + i2;
}
uniform sampler2DMS aaa1;
uniform sampler2DMS aaa2;
