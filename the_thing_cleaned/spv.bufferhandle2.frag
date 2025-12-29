layout(std430) buffer t2 {
    blockType f;
    blockType g;
} t;
void main() {
    blockType b1[2] = blockType[2](t.f, t.g);
    b1[0].a = b1[1].b;
    blockType b2 = t.f;
    blockType b3 = t.g;
    b2.a = b3.b;
}
