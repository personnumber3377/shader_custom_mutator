
uniform something {
    int a;
    int b;
} uSomething;

uniform int y;

void main() {
    int x = uSomething.a + uSomething.b + y;
}
