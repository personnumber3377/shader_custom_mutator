layout(set = 0, binding = 0) uniform SRC_RESOURCE(SRC_RESOURCE_NAME) src;
layout(location = 0) out DstType dst;
void main()
{
    ivec2 srcSubImageCoords = transformImageCoords(ivec2(gl_FragCoord.xy));
    SrcType srcValue = texelFetch(src, params.srcOffset + srcSubImageCoords, params.srcMip);
    SrcType srcValue = texelFetch(src, ivec3(params.srcOffset + srcSubImageCoords, params.srcLayer), params.srcMip);
    dst = transformSrcValue(srcValue);
}
