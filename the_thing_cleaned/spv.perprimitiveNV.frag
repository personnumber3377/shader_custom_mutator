layout(location=0)
in B {
    perprimitiveNV float f;
};
layout(location=4)
in C {
    flat centroid float h;
};
layout(location=8)
out float g;
void main()
{
    g = f + h;
}
