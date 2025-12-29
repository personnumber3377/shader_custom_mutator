layout(binding=0) buffer nontemporal NONTEMPORAL_BUFFER {
    int b_i;
    int b_o;
};
layout(binding=2) uniform nontemporal NONTEMPORAL_UNIFORMS {
    ivec2 u_uv;
};
layout(binding=3) buffer nontemporal NONTEMPORAL_ATOMIC {
    int bn_atom;
};
layout(binding=5, rgba8) uniform readonly image2D u_image;
layout(location=0) out vec4 out_color;
void main() {
    b_o = b_i;
    bntemp_i = bntemp_o;
    atomicAdd(bn_atom, 1);
    atomicAdd(b_natom, 1);
    atomicAdd(b_atom, 1);
}
