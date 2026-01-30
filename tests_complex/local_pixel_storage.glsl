HEADER: frag 3 6
#version 310 es
#extension GL_ANGLE_shader_pixel_local_storage : require

layout(binding = 0, rgba8) uniform pixelLocalANGLE pls0;

void main()
{
    vec4 v = pixelLocalLoadANGLE(pls0);
    pixelLocalStoreANGLE(pls0, v);
}