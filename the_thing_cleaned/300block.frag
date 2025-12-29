precision mediump float;
struct S {
    vec4 u;
    uvec4 v;
    lowp isampler3D sampler;
    vec3 w;
    struct T1 {
        int a;
    } t;
};
uniform S s;
uniform fooBlock {
    uvec4 bv;
    uniform mat2 bm2;
    lowp isampler2D sampler;
    struct T2 {
        int a;
    } t;
    S fbs;
};
uniform barBlock {
    uvec4 nbv;
    int ni;
} inst;
uniform barBlockArray {
    uvec4 nbv;
    int ni;
} insts[4];
uniform unreferenced {
    float f;
    uint u;
};
void main()
{
    texture(s.sampler, vec3(inst.ni, bv.y, insts[2].nbv.z));
    insts[s.v.x];
    fooBlock;
    mat4(s);
    int insts;
    float barBlock;
    mat4(barBlock);
    mat4(unreferenced);
    ++s;
    inst - 1;
    ++barBlock;
    2 * barBlockArray;
}
int fooBlock;
