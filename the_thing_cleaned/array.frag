float gu[];
float g4[4];
float g5[5];
uniform int a;
float[4] foo(float a[5])
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
    gu[2] = 4.0;
    gu[3] = 3.0;
    gu[a] = 5.0;
    g4 = foo(g5);
    g5 = g4;
    gu = g4;
    foo(gu);
    bar(g5);
    if (float[4](1.0, 2.0, 3.0, 4.0) == g4)
        gu[0] = 2.0;
    float u[];
    u[2] = 3.0;
    float u[5];
    u[5] = 5.0;
    foo(u);
    gl_FragData[1000] = vec4(1.0);
    gl_FragData[-1] = vec4(1.0);
    gl_FragData[3] = vec4(1.0);
    const int ca[] = int[](3, 2);
    int sum = ca[0];
    sum += ca[1];
    sum += ca[2];
    const int ca3[3] = int[](3, 2);
    int ica[] = int[](3, 2);
    int ica3[3] = int[](3, 2);
    ica[3.1] = 3;
    ica[u[1]] = 4;
}
int[] foo213234();
int foo234234(float[]);
int foo234235(vec2[] v);
vec3 guns[];
float f = guns[7];
void foo()
{
    int uns[];
    uns[3] = 40;
    uns[1] = 30;
    guns[2] = vec3(2.4);
    float unsf[];
    bar(unsf);
}
float[] foo2()
{
    float f[];
    return f;
    float g[9];
    return g;
}
float gUnusedUnsized[];
void foo3()
{
    float resize1[];
    resize1[2] = 4.0;
    resize1.length();
    float resize1[3];
    resize1.length();
    float resize2[];
    resize2[5] = 4.0;
    float resize2[5];
    resize2.length();
    resize2[5] = 4.0;
}
int[] i = int[]();
float emptyA[];
float b = vec4(emptyA);
uniform sampler2D s2d[];
void foo4()
{
    s2d[a];
    float local[] = gUnusedUnsized;
}
