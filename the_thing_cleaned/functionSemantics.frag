uniform float u;
int foo(int a, const int b, in int c, const in int d, out int e, inout int f)
{
    int sum = a + b + c + d + f;
	a *= 64;
	c *= 64;
	e = 64 * 16;
	f *= 64;
	sum += a + 64 * b + c + 64 * d + e + f;
	return sum;
}
int foo2(float a, vec3 b, out int r)
{
    r = int(3.0 * a);
    return int(5.0 * b.y);
}
int foo3()
{
    if (u > 3.2) {
        discard;
        return 1000000;
    }
    return 2000000;
}
void main()
{
    int e;
	int t = 2;
	struct s {
	    ivec4 t;
	} f;
	f.t.y = 32;
    int color = foo(1, 2, t+t, 8, e, f.t.y);
	color += 128 * (e + f.t.y);
    float arg;
    float ret;
    ret = foo2(4, ivec3(1,2,3), arg);
    color += int(ret + arg);
    color += foo3();
    gl_FragColor = vec4(color);
}
vec3 m(vec2);
void aggCall()
{
    float F;
    m(ivec2(F));
}
vec4 badConv()
{
    return u;
}
