layout(location = 0) out uvec4 data;
void main (void)
{
  data = uvec4(gl_WarpsPerSMNV, gl_SMCountNV, gl_WarpIDNV, gl_SMIDNV);
}
