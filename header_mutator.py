import struct
import random

HEADER_SIZE = 128

GL_FRAGMENT_SHADER = 0x8B30
GL_VERTEX_SHADER   = 0x8B31

# These are numeric enum values in ANGLE:
SH_GLES2_SPEC   = 0
SH_WEBGL_SPEC   = 1
SH_GLES3_SPEC   = 2
SH_WEBGL2_SPEC  = 3

# Outputs (from your enum)
SH_ESSL_OUTPUT                 = 1
SH_GLSL_COMPATIBILITY_OUTPUT   = 2
SH_GLSL_130_OUTPUT             = 3
SH_GLSL_140_OUTPUT             = 4
SH_GLSL_150_CORE_OUTPUT        = 5
SH_GLSL_330_CORE_OUTPUT        = 6
SH_GLSL_400_CORE_OUTPUT        = 7
SH_GLSL_410_CORE_OUTPUT        = 8
SH_GLSL_420_CORE_OUTPUT        = 9
SH_GLSL_430_CORE_OUTPUT        = 10
SH_GLSL_440_CORE_OUTPUT        = 11
SH_GLSL_450_CORE_OUTPUT        = 12
SH_HLSL_3_0_OUTPUT             = 13
SH_HLSL_4_1_OUTPUT             = 14
SH_SPIRV_VULKAN_OUTPUT         = 15
SH_MSL_METAL_OUTPUT            = 16
SH_WGSL_OUTPUT                 = 17

VALID_TYPES = [GL_VERTEX_SHADER, GL_FRAGMENT_SHADER]
VALID_SPECS = [SH_GLES2_SPEC, SH_WEBGL_SPEC, SH_GLES3_SPEC, SH_WEBGL2_SPEC]

# Keep this aligned with translator_fuzzer.cpp validOutputs
VALID_OUTPUTS = [
    SH_ESSL_OUTPUT,
    SH_GLSL_COMPATIBILITY_OUTPUT,
    SH_GLSL_130_OUTPUT,
    SH_GLSL_140_OUTPUT,
    SH_GLSL_150_CORE_OUTPUT,
    SH_GLSL_330_CORE_OUTPUT,
    SH_GLSL_400_CORE_OUTPUT,
    SH_GLSL_410_CORE_OUTPUT,
    SH_GLSL_420_CORE_OUTPUT,
    SH_GLSL_430_CORE_OUTPUT,
    SH_GLSL_440_CORE_OUTPUT,
    SH_GLSL_450_CORE_OUTPUT,
    SH_SPIRV_VULKAN_OUTPUT,
    SH_HLSL_3_0_OUTPUT,
    SH_HLSL_4_1_OUTPUT,
    # Add these AFTER you enable them in the harness:
    SH_MSL_METAL_OUTPUT,
    SH_WGSL_OUTPUT,
]

def mutate_header_precise(header: bytes, rng: random.Random,
                          p_mutate_type=0.10,
                          p_mutate_spec=0.15,
                          p_mutate_output=0.25) -> bytes:
    if len(header) != HEADER_SIZE:
        return header

    h = bytearray(header)

    # Read first 3 uint32
    shader_type, spec, output = struct.unpack_from("<III", h, 0)

    # Mutate fields with controlled probability
    if rng.random() < p_mutate_type:
        shader_type = rng.choice(VALID_TYPES)

    if rng.random() < p_mutate_spec:
        spec = rng.choice(VALID_SPECS)

    if rng.random() < p_mutate_output:
        output = rng.choice(VALID_OUTPUTS)

    # Write back
    struct.pack_into("<III", h, 0, shader_type, spec, output)

    # Force objectCode = true (byte 12 is first byte of the 4th uint32 after III)
    # In your repro: header_list[12] |= 0x01
    h[12] |= 0x01

    # Optional: keep the rest stable for now (don't randomize compile options).
    return bytes(h)
