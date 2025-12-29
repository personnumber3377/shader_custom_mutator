in vec4 inVar;
layout(location=0, index=0) out vec4 outVar;
varying vec4 varyingVar;
void main()
{
    gl_FragColor = varyingVar;
    gl_FragData[1] = inVar;
    int buffer = 4;
}
in gl_PerFragment {
    vec4 gl_Color;
};
void foo()
{
    vec4 c = gl_Color;
    outVar = inVar;
}
in gl_block {
    int gl_i;
} gl_name;
in myBlock {
    int gl_i;
} gl_name;
in gl_PerVertex {
    vec4 gl_FragCoord;
} gl_in[];
in gl_PerVertex {
    vec4 gl_FragCoord;
};
const int start = 6;
layout(location = -2) in vec4 v1;
layout(location = start + 2) in vec4 v2;
layout(location = 4.7e10) in vec4 v20;
layout(location = +60) in float v21;
layout(location = (2)) in float v22;
struct S {
    float f1;
    layout(location = 3) float f2;
};
layout(location = 1) in inblock {
    float f1;
    layout(location = 3) float f2;
};
layout(location = 28) in inblock2 {
    bool b1;
    float f1;
    layout(location = 25) float f2;
    vec4 f3;
    layout(location = 21) S2 s2;
    vec4 f4;
    vec4 f5;
} ininst2;
layout(index=0) out vec4 outVar2;
layout(location=0, index=1) out vec4 outVar3;
layout(location=0, index=1) out vec4 outVar4;
layout(location=27, index=0) in vec4 indexIn;
layout(location=26, index=0) out indexBlock { int a; } indexBlockI;
int precise;
struct SKeyMem { int precise; } KeyMem;
void fooKeyMem()
{
    KeyMem.precise;
}
layout(location=28, index=2) out vec4 outIndex2;
layout(location=4) uniform vec4 ucolor0;
layout(location=5) uniform vec4 ucolor1;
layout(location=6) uniform ColorsBuffer
{
    vec4 colors[128];
} colorsBuffer;
void testOverload() {
    float overloadTest = 42;
    overloadTest = smoothstep(0, 1, overloadTest);
}
