DEFINE_TEXTURE(test_texture)
float4 main(float4 input : TEXCOORD0) : SV_TARGET
{
    float4 tex = SAMPLE_TEXTURE(test_texture2, input.xy);
    return tex;
}
