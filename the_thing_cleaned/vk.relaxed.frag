out vec4 o;
uniform vec4 a;
uniform vec2 b = vec2(0, 0);
layout(location = 0) uniform vec2 c;
uniform vec4 d[10];
struct SamplerArray{
    sampler2D tn[4];
};
uniform struct e {
    vec2 x;
    float y;
    uint z;
    sampler2D t0;
    SamplerArray samplers;
} structUniform;
uniform sampler2D t1;
layout(packed) buffer BufferBlock {
    float j;
    vec4 k;
} bufferInstance;
layout(binding = 0) uniform atomic_uint counter1;
layout(binding = 0) uniform atomic_uint counter2;
layout(binding = 1) uniform atomic_uint counter3;
uint bar() {
    uint j = 0;
    j = atomicCounterIncrement(counter1);
    j = atomicCounterDecrement(counter1);
    j = atomicCounter(counter1);
    j = atomicCounterAdd(counter1, 1);
    j = atomicCounterAdd(counter1, -1);
    j = atomicCounterSubtract(counter1, 1);
    j = atomicCounterMin(counter1, j);
    j = atomicCounterMax(counter1, j);
    j = atomicCounterAnd(counter1, j);
    j = atomicCounterOr(counter1, j);
    j = atomicCounterXor(counter1, j);
    j = atomicCounterExchange(counter1, j);
    j = atomicCounterCompSwap(counter1, 0, j);
    atomicCounterIncrement(counter2);
    atomicCounterIncrement(counter3);
    memoryBarrierAtomicCounter();
    return j;
}
vec4 foo() {
    float f = j + bufferInstance.j + structUniform.y + structUniform.z;
    vec2 v2 = b + c + structUniform.x;
    vec4 v4 = a + d[0] + d[1] + d[2] + k + bufferInstance.k + texture(t1, vec2(0, 0)) + texture(structUniform.t0, vec2(0, 0));
    return vec4(f) * vec4(v2, 1, 1) * v4;
}
vec4 baz(SamplerArray samplers) {
    return texture(samplers.tn[0], vec2(0, 0)) + texture(samplers.tn[1], vec2(0, 0)) + texture(samplers.tn[2], vec2(0, 0)) + texture(samplers.tn[3], vec2(0, 0));
}
void main() {
    float j = float(bar());
    o = j * foo() + baz(structUniform.samplers);
}
