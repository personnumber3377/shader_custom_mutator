precision highp float;
layout (location = 0) in vec4 v_texcoord;
layout (location = 0) out vec4 fragColor;
layout(set = 0, binding = 0) uniform texture2DArray tex2DArray_weights;
layout(set = 0, binding = 1) uniform texture2D tex2D_src1;
layout(set = 0, binding = 2) uniform texture2D tex2D_src2;
layout(set = 0, binding = 3) uniform sampler samp;
layout(set = 0, binding = 4) uniform sampler2D tex_samp;
layout(set = 0, binding = 5) uniform sampler2DArray tex_samp_array;
void main()
{
    fragColor = textureWeightedQCOM(
                    sampler2D(tex2D_src1, samp),
                    v_texcoord.xy,
                    sampler2DArray(tex2DArray_weights, samp));
    fragColor = textureWeightedQCOM(
                    tex_samp,
                    v_texcoord.xy,
                    tex_samp_array);
}
