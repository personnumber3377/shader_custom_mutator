struct S
{
	highp ivec3 a;
	mediump mat3 b[4];
	highp vec4 c;
};
layout(std430) buffer T4 {
    T1 t1;
    T2 t2;
    T3 t3;
} t4;
layout(location = 0) flat in int i;
void main()
{
    vec3 y;
    y = t4.t1.x[i];
    y = t4.t2.x[i][i][i];
    mat3 z = t4.t3.s.b[0];
}
