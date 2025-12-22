layout(set = 0, binding = 0) uniform SRC_RESOURCE_NAME src;
layout(location = 0) out DstType dst;
void main()
{
    ivec2 srcSubImageCoords = transformImageCoords(ivec2(gl_FragCoord.xy));
    SrcType srcValue = texture(
        src, vec2((params.srcOffset + srcSubImageCoords) + vec2(0.5)) / textureSize(src, 0), params.srcMip);
    SrcType srcValue = SrcType(0);
    for (int i = 0; i < params.srcSampleCount; i++)
    {
        srcValue += texelFetch(src, ivec2(params.srcOffset + srcSubImageCoords), i);
    }
    srcValue /= params.srcSampleCount;
    dst = transformSrcValue(srcValue);
}
