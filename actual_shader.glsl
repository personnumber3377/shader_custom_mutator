#version 450 core

//#extension GL_GOOGLE_include_directive : require
//#extension GL_EXT_samplerless_texture_functions : require

// layout(set = 0, binding = 0)uniform texture2D src;
// layout(location = 0)out uvec4 dst;

#line 1 "shaders/src/ImageCopy.inc"

struct foo
{
    vec3 a;
    vec2 b;
    float c[100];
};

struct bar
{
    foo a, b, c;
} a, b, c;


float linearToSRGB(float linear)
{
    bar a, b, c;

    if(linear <= 0.0031308)
    {
        return linear * 12.92;
    }
    else
    {
        return pow(linear,(1.0f / 2.4f))* 1.055f - 0.055f;
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
#line 56 "shaders/src/ImageCopy.frag"

void main()
{
    ivec2 srcSubImageCoords = transformImageCoords(ivec2(gl_FragCoord . xy));

          vec4 srcValue = texelFetch(src, params . srcOffset + srcSubImageCoords, params . srcMip);

    dst = transformSrcValue(srcValue);
}
