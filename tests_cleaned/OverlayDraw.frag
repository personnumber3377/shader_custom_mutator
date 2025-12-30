precision mediump float;
precision mediump int;

uint getChar(const uvec2 coordInWidget, const uint fontGlyphWidth)
{
    const uint charIndex = coordInWidget.x / fontGlyphWidth;
    const uint packIndex = charIndex / 4;
    const uvec4 arrayItem = textWidgetsData[widgetIndex].text[packIndex / 4];
    const uint col = packIndex % 4;
    uint packedChars;
    if (col == 0)
    {
        packedChars = arrayItem[0];
    }
    else if (col == 1)
    {
        packedChars = arrayItem[1];
    }
    else if (col == 2)
    {
        packedChars = arrayItem[2];
    }
    else
    {
        packedChars = arrayItem[3];
    }
    const uint shift = (charIndex % 4) * 8;
    return (packedChars >> (24 - shift)) & 0xFF;
}
float sampleFont(const uint textChar,
                 const uvec2 coordInWidget,
                 const uvec2 fontGlyphSize,
                 const uint fontMip)
{
    const uvec2 coordInGlyph = coordInWidget % fontGlyphSize;
    return texelFetch(font, ivec3(coordInGlyph, textChar), int(fontMip)).x;
}
vec4 renderText(uvec2 coordInWidget)
{
    const uvec4 fontSizePacked = textWidgetsData[widgetIndex].fontSize;
    const uvec2 fontGlyphSize = fontSizePacked.xy;
    const uint fontMip = fontSizePacked.z;
    const uint textChar = getChar(coordInWidget, fontGlyphSize.x);
    if (textChar >= FONT_CHARACTERS)
    {
        return vec4(0);
    }
    const float sampleValue = sampleFont(textChar, coordInWidget, fontGlyphSize, fontMip);
    vec4 result = vec4(0, 0, 0, 0.4);
    result = mix(result, textWidgetsData[widgetIndex].color, sampleValue);
    return result;
}
uint getValue(const uvec2 coordInWidget, const uint valueWidth)
{
    const uint valueIndex = coordInWidget.x / valueWidth.x;
    const uvec4 arrayItem = graphWidgetsData[widgetIndex].values[valueIndex / 4];
    const uint col = valueIndex % 4;
    if (col == 0)
    {
        return arrayItem[0];
    }
    else if (col == 1)
    {
        return arrayItem[1];
    }
    else if (col == 2)
    {
        return arrayItem[2];
    }
    else
    {
        return arrayItem[3];
    }
}
vec4 renderGraph(uvec2 coordInWidget)
{
    const uvec4 widgetCoords = graphWidgetsData[widgetIndex].coordinates;
    if (coordInWidget.x == 0 || coordInWidget.y == 0 ||
        coordInWidget.x + 1 == (widgetCoords.z - widgetCoords.x) ||
        coordInWidget.y + 1 == (widgetCoords.w - widgetCoords.y))
    {
        return vec4(0, 0, 0, 1);
    }
    const uint valueWidth = graphWidgetsData[widgetIndex].valueWidth.x;
    const uint value = getValue(coordInWidget, valueWidth);
    const uint widgetHeight = widgetCoords.w - widgetCoords.y;
    bool indicateOverflow = value > widgetHeight && coordInWidget.y + 4 >= widgetHeight
            && ((coordInWidget.x ^ coordInWidget.y) & 1) == 0;
    if ((widgetHeight - coordInWidget.y) >= value || indicateOverflow)
    {
        return vec4(0);
    }
    return graphWidgetsData[widgetIndex].color;
}
void main()
{
    const uvec4 widgetCoords = params.isText
        ? textWidgetsData[widgetIndex].coordinates
        : graphWidgetsData[widgetIndex].coordinates;
    uvec2 fragCoords = uvec2(floor(gl_FragCoord.xy));
    if (params.rotateXY)
    {
        fragCoords.x = params.viewportSize.x - 1 - fragCoords.x;
        fragCoords = fragCoords.yx;
    }
    const uvec2 coordInWidget = fragCoords - widgetCoords.xy;
    if (any(lessThan(coordInWidget, uvec2(0))) ||
        any(greaterThanEqual(coordInWidget, widgetCoords.zw - widgetCoords.xy)))
    {
        color = vec4(1, 0, 1, 1);
        return;
    }
    if (params.isText)
    {
        color = renderText(coordInWidget);
    }
    else
    {
        color = renderGraph(coordInWidget);
    }
}
