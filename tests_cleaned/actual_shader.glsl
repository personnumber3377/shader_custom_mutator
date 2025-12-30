precision mediump float;
precision mediump int;

float linearToSRGB(float linear)
{
    if(linear <= 0.0031308)
    {
        return linear * 12.92;
    }
    else
    {
        return pow(linear,(1.0 / 2.4))* 1.055 - 0.055;
    }
}
ivec2 transformImageCoords(ivec2 glFragCoords)
{
    ivec2 imageCoordsOut = glFragCoords - params . dstOffset;
    if(params . flipX)
    {
        imageCoordsOut . x = - imageCoordsOut . x;
    }
    if(params . flipY)
    {
        imageCoordsOut . y = - imageCoordsOut . y;
    }
    if(params . rotateXY)
    {
        imageCoordsOut . xy = imageCoordsOut . yx;
    }
    return imageCoordsOut;
}
      uvec4 transformSrcValue(vec4 srcValue)
{
    if(params . srcIsSRGB)
    {
        srcValue . r = linearToSRGB(srcValue . r);
        srcValue . g = linearToSRGB(srcValue . g);
        srcValue . b = linearToSRGB(srcValue . b);
    }
    if(params . premultiplyAlpha)
    {
        srcValue . rgb *= srcValue . a;
    }
    else if(params . unmultiplyAlpha && srcValue . a > 0)
    {
        srcValue . rgb /= srcValue . a;
    }
    srcValue *= 255.0;
          uvec4 dstValue = uvec4(srcValue);
    if(params . dstHasLuminance)
    {
        dstValue . rg = dstValue . ra;
    }
    else if(params . dstIsAlpha)
    {
        dstValue . r = dstValue . a;
    }
    else
    {
        int defaultChannelsMask = params . dstDefaultChannelsMask;
        if((defaultChannelsMask & 2)!= 0)
        {
            dstValue . g = 0;
        }
        if((defaultChannelsMask & 4)!= 0)
        {
            dstValue . b = 0;
        }
        if((defaultChannelsMask & 8)!= 0)
        {
            dstValue . a = 1;
        }
    }
    return dstValue;
}
void main()
{
    ivec2 srcSubImageCoords = transformImageCoords(ivec2(gl_FragCoord . xy));
          vec4 srcValue = texelFetch(src, params . srcOffset + srcSubImageCoords, params . srcMip);
    dst = transformSrcValue(srcValue);
}
