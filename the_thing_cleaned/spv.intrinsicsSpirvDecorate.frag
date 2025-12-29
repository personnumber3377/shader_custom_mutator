spirv_decorate (extensions = ["SPV_AMD_shader_explicit_vertex_parameter"], 11, 4992)
in vec2 gl_BaryCoordNoPerspAMD;
spirv_decorate (extensions = ["SPV_AMD_shader_explicit_vertex_parameter"], 11, 4993)
in vec2 gl_BaryCoordNoPerspCentroidAMD;
spirv_decorate (extensions = ["SPV_AMD_shader_explicit_vertex_parameter"], 11, 4994)
in vec2 gl_BaryCoordNoPerspSampleAMD;
spirv_decorate (extensions = ["SPV_AMD_shader_explicit_vertex_parameter"], 11, 4995)
in vec2 gl_BaryCoordSmoothAMD;
spirv_decorate (extensions = ["SPV_AMD_shader_explicit_vertex_parameter"], 11, 4996)
in vec2 gl_BaryCoordSmoothCentroidAMD;
spirv_decorate (extensions = ["SPV_AMD_shader_explicit_vertex_parameter"], 11, 4997)
in vec2 gl_BaryCoordSmoothSampleAMD;
spirv_decorate (extensions = ["SPV_AMD_shader_explicit_vertex_parameter"], 11, 4998)
in vec3 gl_BaryCoordPullModelAMD;
spirv_instruction(extensions = ["SPV_AMD_shader_explicit_vertex_parameter"], set = "SPV_AMD_shader_explicit_vertex_parameter", id = 1)
float interpolateAtVertexAMD(float interpolant, uint vertexIdx);
layout(location = 0) in __explicitInterpAMD float floatIn;
layout(location = 0) out float floatOut;
layout(location = 1) out vec2 vec2Out;
void main()
{
    floatOut = interpolateAtVertexAMD(floatIn, 1);
    vec2Out = gl_BaryCoordNoPerspAMD + gl_BaryCoordNoPerspCentroidAMD + gl_BaryCoordNoPerspSampleAMD +
              gl_BaryCoordSmoothAMD + gl_BaryCoordSmoothCentroidAMD + gl_BaryCoordSmoothSampleAMD +
              gl_BaryCoordPullModelAMD.xy;
}
