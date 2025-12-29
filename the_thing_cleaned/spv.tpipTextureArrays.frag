precision highp float;
layout (location = 0) in vec4 v_texcoord;
layout (location = 0) out vec4 fragColor;
layout(set = 0, binding = 3) uniform sampler samp;
layout(set = 0, binding = 4) uniform texture2D tex2D_srcs[8];
layout(set = 0, binding = 5) uniform sampler2D samplers[3];
void main()
{
    uvec2 tgt_coords; tgt_coords.x = uint(v_texcoord.x); tgt_coords.x = uint(v_texcoord.y);
    uvec2 ref_coords; ref_coords.x = uint(v_texcoord.z); ref_coords.y = uint(v_texcoord.w);
    uvec2 blockSize = uvec2(4, 4);
    uint  ii = tgt_coords.x % 8;
    fragColor = textureBlockMatchSSDQCOM(
                    samplers[0],
                    tgt_coords,
                    sampler2D(tex2D_srcs[ii], samp),
                    ref_coords,
                    blockSize);
    fragColor = textureBlockMatchSADQCOM(
                    sampler2D(tex2D_srcs[1], samp),
                    tgt_coords,
                    samplers[1],
                    ref_coords,
                    blockSize);
}
