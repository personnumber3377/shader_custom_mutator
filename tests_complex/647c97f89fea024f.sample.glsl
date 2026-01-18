HEADER: frag 4 10
#version 310 es
layout(local_size_x=1, local_size_y=1, local_size_z=1) in;
layout(r32ui, binding = 0) readonly uniform highp uimage2D uImage_1;
layout(r32ui, binding = 1) writeonly uniform highp uimage2D uImage_2;
void main()
{
    uvec4 value = imageLoad(uImage_1, ivec2(gl_LocalInvocationID.xy));
    imageStore(uImage_2, ivec2(gl_LocalInvocationID.xy), value);
}