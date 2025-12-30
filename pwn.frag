uniform struct S1 { samplerCube ar; } a1;
uniform struct S2 { S1 s; } a2;

vec4 v;

void main (void)
{
    v = textureCube(a2.s.ar, vec3(1.0));
}
