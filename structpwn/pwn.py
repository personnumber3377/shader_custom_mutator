# repro.py

import struct
import sys

shader_type = 0x8B31  # GL_VERTEX_SHADER
shader_spec = 2       # SH_GLES3_SPEC
output_format = 15    # SH_SPIRV_VULKAN_OUTPUT

header_list = list(struct.pack('<III', shader_type, shader_spec, output_format))
header_list.extend([0] * (128 - len(header_list)))
header_list[12] |= 0x01 # objectCode = true
header = bytes(header_list)


shader_source_old = r'''
uniform struct S1 { samplerCube ar; } a1;
uniform struct S2 { S1 s; } a2;

vec4 v;

void main (void)
{
    v = textureCube(a2.s.ar, vec3(1.0,  1.0, 1.0));
}'''


shader_source = r'''
precision mediump float;
precision mediump int;

uniform struct S1 {
  samplerCube ar;
} a1;

uniform struct S2 {
  S1 s;
} a2;

void main()
{
  textureCube(a2.s.ar, vec3(1.0,  1.0, 1.0));
}'''



shader_newest = r'''
precision mediump float;
precision mediump int;

struct S1 {
  samplerCube ar;
} a1;

uniform struct S2 {
  S1 s;
} a2;

void main()
{
  textureCube(a2.s.ar, vec3(1.0,  1.0, 1.0));
}'''


# // v = textureCube(a2.s.ar, vec3(1.0));

sys.stdout.buffer.write(header + shader_newest.encode('ascii') + b'\x00')
