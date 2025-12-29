void foo(bvec4 paramb4, out bvec2 paramb2)
{
    bool b1 = paramb4.z;
    paramb2 = bvec2(b1);
}
layout(location = 0) out vec4 fragColor;
void main()
{
    b2 = bvec2(0.0);
    if (b4.z)
        b2 = bvec2(b4.x);
    if (b2.x)
        foo(b4, b2);
    fragColor  = vec4(b4.x && b4.y);
    fragColor -= vec4(b4.x || b4.y);
}
