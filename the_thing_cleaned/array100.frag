float gu[];
float g4[4];
float g5[5];
uniform int a;
float[4] foo(float[5] a)
{
    return float[](a[0], a[1], a[2], a[3]);
}
void bar(float[5]) {}
void main()
{
    {
        float gu[2];
        gu[2] = 4.0;
    }
    g4 = foo(g5);
    g5 = g4;
    gu = g4;
    foo(gu);
    bar(g5);
    if (float[4](1.0, 2.0, 3.0, 4.0) == g4)
        gu[0] = 2.0;
    float u[5];
    u[5] = 5.0;
    foo(u);
    gl_FragData[1000] = vec4(1.0);
    gl_FragData[-1] = vec4(1.0);
    gl_FragData[3] = vec4(1.0);
}
struct SA {
    vec3 v3;
    vec2 v2[4];
};
struct SB {
    vec4 v4;
    SA sa;
};
SB bar9()
{
    SB s;
    return s;
}
void bar10(SB s)
{
}
void bar11()
{
    SB s1, s2;
    s1 = s2;
    bar10(s1);
    s2 = bar9();
    SB initSb = s1;
}
