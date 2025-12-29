layout(std430) buffer t2 {
    blockType f;
    blockType g;
} t;
flat in uvec2 h, i;
void main() {
    blockType b1[2] = blockType[2](blockType(h), blockType(i));
    b1[0].a = b1[1].b;
    blockType b2 = blockType(h);
    blockType b3 = blockType(i);
    b2.a = b3.b;
    uvec2 j = uvec2(b2);
    uint carry;
    j.x = uaddCarry(j.x, 256, carry);
    j.y += carry;
    b2 = blockType(j);
}
