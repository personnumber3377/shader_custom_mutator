layout(set = 1, binding = 2, std140) uniform t4 {
    layout(offset = 0)  int j;
    t3 k;
} x;
void main() {
    x.k.h = x.j;
}
