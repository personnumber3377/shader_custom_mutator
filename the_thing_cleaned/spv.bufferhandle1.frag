layout(std430) buffer t2 {
    blockType f;
    blockType g;
} t;
void main() {
    t.f.b = t.g.a;
    blockType j = t.f;
    j.d = j.c;
    j.d = j.f[1];
    j.d = j.g.y;
}
