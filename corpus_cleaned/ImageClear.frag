layout(push_constant) uniform PushConstants {
    Type clearColor;
    float clearDepth;
} params;
layout(location = ATTACHMENT) out Type colorOut;
void main()
{
    colorOut = params.clearColor;
    gl_FragDepth = params.clearDepth;
}
