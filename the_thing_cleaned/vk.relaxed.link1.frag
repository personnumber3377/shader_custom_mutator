out vec4 o;
uniform vec4 a;
uniform vec2 b1;
uniform vec2 b2;
uniform vec4 c1;
uniform vec4 d;
layout (binding = 0) uniform atomic_uint counter1;
layout (binding = 0) uniform atomic_uint counter2;
vec4 foo();
vec4 bar() {
    uint j = atomicCounterIncrement(counter1) + atomicCounterDecrement(counter2);
    vec4 v = a + vec4(b1.x, b1.y, b2.x, b2.y) + c1 + d;
    return float(j) * v;
}
void main() {
    o = foo() + bar();
}
