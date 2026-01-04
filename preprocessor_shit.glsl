HEADER: frag 2 15
#version 300 es
precision highp float;
out vec4 outColor;

layout(std140, column_major) uniform Ubo
{
    mat4 m1;
    layout(row_major) mat4 m2;
} ubo[3];

#define EXPECT(result, expression, value) if ((expression) != value) { result = false; }

#define VERIFY_IN(result, mat, cols, rows)                  \
    for (int c = 0; c < cols; ++c)                          \
    {                                                       \
        for (int r = 0; r < rows; ++r)                      \
        {                                                   \
            EXPECT(result, mat[c][r], float(c * 4 + r));    \
        }                                                   \
    }

void main()
{
    bool result = true;

    VERIFY_IN(result, ubo[0].m1, 4, 4);
    VERIFY_IN(result, ubo[0].m2, 4, 4);

    VERIFY_IN(result, ubo[1].m1, 4, 4);
    VERIFY_IN(result, ubo[1].m2, 4, 4);

    VERIFY_IN(result, ubo[2].m1, 4, 4);
    VERIFY_IN(result, ubo[2].m2, 4, 4);

    outColor = result ? vec4(0, 1, 0, 1) : vec4(1, 0, 0, 1);
}