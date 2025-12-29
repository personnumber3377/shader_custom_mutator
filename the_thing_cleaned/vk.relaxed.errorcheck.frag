layout (location = 0) in vec4 io;
out vec4 o;
uniform vec4 a;
uniform float test;
uniform vec2 test;
vec4 foo() {
    return a + vec4(test);
}
void main() {
    o = io + foo();
}
