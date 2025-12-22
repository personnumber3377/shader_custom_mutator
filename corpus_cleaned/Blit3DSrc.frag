layout(set = 0, binding = 0) uniform COLOR_SRC_RESOURCE(SRC_RESOURCE_NAME) color;
layout(location = 0) out ColorType colorOut0;
layout(location = 1) out ColorType colorOut1;
layout(location = 2) out ColorType colorOut2;
layout(location = 3) out ColorType colorOut3;
layout(location = 4) out ColorType colorOut4;
layout(location = 5) out ColorType colorOut5;
layout(location = 6) out ColorType colorOut6;
layout(location = 7) out ColorType colorOut7;
layout(set = 0, binding = 2) uniform sampler blitSampler;
void main()
{
    CoordType srcImageCoordsXY = getSrcImageCoords();
    vec3 srcImageCoords = vec3(srcImageCoordsXY, params.srcLayer);
    ColorType colorValue = COLOR_TEXEL_FETCH(color, srcImageCoords, 0);
    broadcastColor(colorValue);
}
