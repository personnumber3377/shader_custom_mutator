layout(depth_any) out float gl_FragDepth;
layout(depth_greater) out float gl_FragDepth;
void main()
{
    gl_FragDepth = 0.3;
}
layout(depth_less) in float depth;
layout(depth_any) out float gl_FragDepth;
layout(binding=0) uniform atomic_uint a[];
uniform writeonly image2D      i2D;
ivec2 iv2dim = imageSize(i2D);
ivec2 iv2dim1 = imageSize(i2D);
void atomicOpPass()
{
    int origi = atomicAdd(atomi, 3);
    uint origu = atomicAnd(atomu, 7u);
    origi = atomicExchange(atomi, 4);
    origu = atomicCompSwap(atomu, 10u, 8u);
}
