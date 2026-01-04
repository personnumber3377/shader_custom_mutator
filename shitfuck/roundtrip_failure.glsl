HEADER: vert 2 15
#version 300 es
in vec4 inputAttribute;
flat out struct
{
    int field;
} v_s0;
flat out struct
{
    int field;
} v_s1;
flat out struct
{
    int field;
} v_s2, v_s3;
void main()
{
    v_s0.field = 1;
    v_s1.field = 2;
    v_s2.field = 3;
    v_s3.field = 4;
    gl_Position = inputAttribute;
}