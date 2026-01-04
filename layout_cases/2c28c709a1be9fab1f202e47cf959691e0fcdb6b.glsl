HEADER: frag 2 15
#version 300 es
precision highp float;
out vec4 outColor;

layout(std140, column_major) uniform Ubo
{
    mat4 m1;
    layout(row_major) mat4 m2[2];
} ubo;

void main()
{
    bool result = true;

    int x = 0;
    if (x == 1 && ubo.m2[x = 1][1][1] == 5.0)
    {
        // First x == 1 should prevent the side effect of the second expression (x = 1) from
        // being executed.  If x = 1 is run before the if, the condition of the if would be true,
        // which is a failure.
        result = false;
    }
    if (x == 1)
    {
        result = false;
    }

    outColor = result ? vec4(0, 1, 0, 1) : vec4(1, 0, 0, 1);
}