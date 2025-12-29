flat in ivec4 uiv4;
in vec4 uv4;
bool ub;
bool uba;
bvec4 ub41, ub42;
in float uf;
flat in int ui;
out float of1;
out vec4  of4;
bool foo() { ++of1; return of1 > 10.0; }
void main()
{
    of1 = 0.0;
    of4 = vec4(0.0);
    if (ub || ui > 2)
        ++of1;
    if (ub && !uba)
        ++of1;
    if (ub || foo())
        ++of1;
    if (ub && foo())
        ++of1;
    if (foo() || ub)
        ++of1;
    if (foo() && ub)
        ++of1;
    if (ub || ++of1 > 1.0)
        ++of4;
    if (++of1 > 1.0 || ub)
        ++of4;
    if (ub || sin(uf) * 4.0 > of1)
        ++of1;
    if (ub && sin(uf) * 4.0 > of1)
        ++of1;
}
