precision highp float;
layout (location = 0) in vec4 v_texcoord;
layout (location = 0) out vec4 fragColor;
layout(set = 0, binding = 0) uniform texture2DArray tex2DArray_weights;
layout(set = 0, binding = 1) uniform texture2D tex2D_src1;
layout(set = 0, binding = 2) uniform texture2D tex2D_src2;
layout(set = 0, binding = 3) uniform sampler samp;
layout(set = 0, binding = 4) uniform sampler2D tex_samp;
void main()
{
    vec2 boxSize = vec2(2.5, 4.5);
    fragColor = textureBoxFilterQCOM(
                    sampler2D(tex2D_src1, samp),
                    v_texcoord.xy,
                    boxSize);
    fragColor = textureBoxFilterQCOM(
                    tex_samp,
                    v_texcoord.xy,
                    boxSize);
}
