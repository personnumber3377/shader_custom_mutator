precision highp float;
layout (location = 0) in vec4 v_texcoord;
layout (location = 0) out vec4 fragColor;
layout(set = 0, binding = 0) uniform texture2DArray tex2DArray_weights;
layout(set = 0, binding = 1) uniform texture2D tex2D_src1;
layout(set = 0, binding = 2) uniform texture2D tex2D_src2;
layout(set = 0, binding = 3) uniform sampler samp;
layout(set = 0, binding = 4) uniform sampler2D target_samp;
layout(set = 0, binding = 5) uniform sampler2D ref_samp;
void main()
{
    uvec2 tgt_coords; tgt_coords.x = uint(v_texcoord.x); tgt_coords.x = uint(v_texcoord.y);
    uvec2 ref_coords; ref_coords.x = uint(v_texcoord.z); ref_coords.y = uint(v_texcoord.w);
    uvec2 blockSize = uvec2(4, 4);
    fragColor = textureBlockMatchGatherSSDQCOM(
                    sampler2D(tex2D_src1, samp),
                    tgt_coords,
                    sampler2D(tex2D_src2, samp),
                    ref_coords,
                    blockSize);
    fragColor = textureBlockMatchGatherSSDQCOM(
                    target_samp,
                    tgt_coords,
                    ref_samp,
                    ref_coords,
                    blockSize);
}
