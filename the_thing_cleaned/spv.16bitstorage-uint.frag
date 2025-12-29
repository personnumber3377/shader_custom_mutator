struct S
{
    uint16_t  x;
    u16vec2    y;
    u16vec3    z;
};
struct S3 {
    S2 x;
};
layout(row_major, std430) buffer B3
{
    S2 x;
} b3;
layout(column_major, std430) buffer B4
{
    S2 x;
    S3 y;
} b4;
void main()
{
    b2.o = b1.a;
    b2.p = u16vec2(uvec3(b2.q).xy);
    b2.p = u16vec2(uvec3(b5.q).xy);
    b2.r[0] = b2.r[0];
    b2.r[1] = b5.r[1];
    b2.p = b2.p;
    uint x0 = uint(b1.a);
    uvec4 x1 = uvec4(b1.a, b2.p, 1);
    b4.x.x = b3.x.x;
    b2.o = uint16_t(uvec2(b2.p).x);
    b2.p = b2.v[1].y;
    uvec3 v3 = uvec3(b2.w[b1.j], b2.w[b1.j+1], b2.w[b1.j+2]);
    uvec3 u3 = uvec3(b5.w[b1.j], b5.w[b1.j+1], b5.w[b1.j+2]);
    b2.x[0] = b2.x[0];
    b2.x[1] = b5.x[1];
    b2.p.x = b1.a;
    b2.o = b2.p.x;
    b2.p = u16vec2(uvec2(1, 2));
    b2.o = uint16_t(3u);
    b2.o = uint16_t(b1.a);
    b2.p = u16vec2(b1.b);
    b2.q = u16vec3(b1.c);
}
