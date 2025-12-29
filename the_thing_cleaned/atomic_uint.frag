layout(binding = 0) uniform atomic_uint counter;
layout(binding = 0, offset = 9) uniform atomic_uint counter;
uint func(atomic_uint c)
{
    return atomicCounterIncrement(c);
}
uint func2(out atomic_uint c)
{
    return counter;
    return atomicCounter(counter);
}
void main()
{
     atomic_uint non_uniform_counter;
     uint val = atomicCounter(counter);
     atomicCounterDecrement(counter);
}
layout(binding = 1, offset = 3) uniform atomic_uint countArr[4];
uniform int i;
void opac()
{
    counter + counter;
    -counter;
    int a[3];
    a[counter];
    countArr[2];
    countArr[i];
    counter = 4;
}
in atomic_uint acin;
atomic_uint acg;
uniform atomic_uint;
uniform atomic_uint aNoBind;
layout(binding=0, offset=32) uniform atomic_uint aOffset;
layout(binding=0, offset=4) uniform atomic_uint;
layout(binding=0) uniform atomic_uint bar3;
layout(binding=0) uniform atomic_uint ac[2];
layout(binding=0) uniform atomic_uint ad;
layout(offset=8) uniform atomic_uint bar4;
layout(binding = 0, offset = 12) uniform atomic_uint overlap;
layout(binding = 20) uniform atomic_uint bigBind;
