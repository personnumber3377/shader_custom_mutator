layout(set = 0, binding = 0) uniform COLOR_SRC_RESOURCE(SRC_RESOURCE_NAME) color;
layout(location = 0) out ColorType colorOut0;
layout(location = 1) out ColorType colorOut1;
layout(location = 2) out ColorType colorOut2;
layout(location = 3) out ColorType colorOut3;
layout(location = 4) out ColorType colorOut4;
layout(location = 5) out ColorType colorOut5;
layout(location = 6) out ColorType colorOut6;
layout(location = 7) out ColorType colorOut7;
layout(set = 0, binding = 0) uniform DEPTH_SRC_RESOURCE(SRC_RESOURCE_NAME) depth;
layout(set = 0, binding = 1) uniform STENCIL_SRC_RESOURCE(SRC_RESOURCE_NAME) stencil;
layout(set = 0, binding = 2) uniform sampler blitSampler;
void main()
{
    CoordType srcImageCoords = getSrcImageCoords();
    ColorType colorValue = ColorType(0, 0, 0, 0);
    for (int i = 0; i < params.samples; ++i)
    {
        colorValue += COLOR_TEXEL_FETCH(color, srcImageCoords, i);
    }
    colorValue *= params.invSamples;
    colorValue = ColorType(round(colorValue * params.invSamples));
    ColorType colorValue = COLOR_TEXEL_FETCH(color, srcImageCoords, 0);
    broadcastColor(colorValue);
    gl_FragDepth = DEPTH_TEXEL_FETCH(depth, srcImageCoords, 0).x;
    gl_FragStencilRefARB = int(STENCIL_TEXEL_FETCH(stencil, srcImageCoords, 0).x);
}
