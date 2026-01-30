HEADER: frag 3 6
#version 300 es
#extension GL_ANGLE_shader_pixel_local_storage : require
precision highp float;
precision highp int;


layout(binding = 0, rgba8) uniform highp pixelLocalANGLE pls0;

void main()
{
    vec4 v = pixelLocalLoadANGLE(pls0);
    pixelLocalStoreANGLE(pls0, v);
}