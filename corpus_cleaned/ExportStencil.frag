layout(input_attachment_index = 0, set = 0, binding = 0) uniform usubpassInput stencilIn;
layout(push_constant) uniform PushConstants {
    uint bit;
} params;
void main()
{
    uint stencilValue = subpassLoad(stencilIn).x;
    if ((stencilValue >> params.bit & 1u) == 0)
    {
        discard;
    }
}
