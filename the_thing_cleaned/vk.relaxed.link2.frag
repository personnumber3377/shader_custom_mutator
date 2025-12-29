uniform vec4 a;
uniform vec2 b2;
uniform vec2 b1;
uniform vec4 c2;
uniform vec4 d;
layout (binding = 0) uniform atomic_uint counter3;
layout (binding = 0) uniform atomic_uint counter2;
vec4 foo() {
    uint j = atomicCounterIncrement(counter2) + atomicCounterDecrement(counter3);
    vec4 v = a + vec4(b1.x, b1.y, b2.x, b2.y) + c2 + d;
    return float(j) * v;
}
