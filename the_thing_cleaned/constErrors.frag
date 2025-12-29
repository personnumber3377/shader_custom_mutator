in vec4 inVar;
out vec4 outVar;
const int constInt = 3;
uniform int uniformInt;
void main()
{
    const int a1 = 2;
    const int a2 = constInt;
    const int a3 = uniformInt;
    vec4 c[constInt];
    vec4 d[uniformInt];
    vec4 e[constInt + uniformInt];
    vec4 f[uniformInt + constInt];
    vec4 g[int(sin(0.3)) + 1];
}
const struct S {
    vec3 v3;
    ivec2 iv2;
} s = S(vec3(3.0), ivec2(3, constInt + uniformInt));
const struct S2 {
    vec3 v3;
    ivec2 iv2;
    mat2x4 m;
} s2 = S2(vec3(3.0), ivec2(3, constInt), mat2x4(1.0, 2.0, 3.0, inVar.x, 5.0, 6.0, 7.0, 8.0));
const float f = 3;
