HEADER: frag 3 6
#version 300 es

uniform something {
    int a;
    int b;
} uSomething;

uniform int y;

void main() {
    int x = uSomething.a + uSomething.b + y;
}
