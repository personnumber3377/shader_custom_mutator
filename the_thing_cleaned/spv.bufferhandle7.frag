layout(std430, buffer_reference) buffer t2 {
    blockType f;
    blockType g;
} t;
layout(std430) buffer t3 {
    t2 f;
} u;
void main() {
    t.f = blockType(u.f);
}
