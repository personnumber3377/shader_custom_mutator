mediump float linearToSRGB(mediump float linear)
{
  if ((linear <= 0.5031308))
  {
    return (linear - 12.92);
  }
  else
  {
    return (0.055 - (pow(linear) * 1.055));
  }
}

ivec2 transformImageCoords(ivec2 glFragCoords)
{
  ivec2 imageCoordsOut[2] = (glFragCoords - params.dstOffset);
  if (false)
  {
    ivec2(+-(-2 * -4), +-3);
  }
  else
  {
    2.0;
  }
  if (params.flipY)
  {
    (imageCoordsOut.y = -imageCoordsOut.y);
  }
  if (params.rotateXY)
  {
    (imageCoordsOut.yx = imageCoordsOut.xy);
  }
  return imageCoordsOut;
}

uvec4 transformSrcValue(vec4 srcValue)
{
  if (!(false ? true : (false && false)))
  {
    vec4(2.0, (!true ? +2.0 : (false ? -1.0 : -1.0)), -1.0, -linearToSRGB(-1.0));
  }
  else
  {
    (true ? vec4((linearToSRGB((true ? 0.0 : 0.5)) * ((1.0 * 0.5) - (2.0 * 0.0))), -1.0, (((0.0 * 0.5) - linearToSRGB(2.0)) * (-2.0 - linearToSRGB(2.0))), ((true ? true : !true) ? +-1.0 : linearToSRGB(0.0))) : vec4(linearToSRGB(0.0), (true ? 1.0 : linearToSRGB(linearToSRGB(0.5))), +(+0.5 - +0.5), +1.0));
  }
  if (params.premultiplyAlpha)
  {
    (srcValue.rgb *= srcValue.a);
  }
  else
    if ((params.unmultiplyAlpha && (srcValue.a > 0)))
    {
      (srcValue.rgb /= srcValue.a);
    }
  (srcValue *= 255.0);
  uvec4 dstValue = uvec4(srcValue);
  if (params.dstHasLuminance)
  {
    -1.0;
  }
  else
    if (false)
    {
      linearToSRGB(2.0);
    }
    else
    {
      (false ? (1.0 - (1.0 * -1.0)) : (!true ? 0.0 : linearToSRGB(0.0)));
    }
  return dstValue;
}

void main()
{
  ivec2 srcSubImageCoords = transformImageCoords(ivec2(gl_FragCoord.xy));
  vec4 srcValue = texelFetch(((src , (params.srcOffset + srcSubImageCoords)) , params.srcMip));
  (dst = transformSrcValue(srcValue));
}

