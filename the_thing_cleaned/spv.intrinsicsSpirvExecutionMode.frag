spirv_execution_mode(5027);
spirv_decorate(extensions = ["SPV_EXT_shader_stencil_export"], capabilities = [5013], 11, 5014)
out int gl_FragStencilRef;
layout(location = 0) in flat int color;
void main()
{
    gl_FragStencilRef = color;
}
