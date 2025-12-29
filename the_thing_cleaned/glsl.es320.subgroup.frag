layout(location = 0) out uvec4 data;
void main (void)
{
  data = uvec4(gl_SubgroupSize, gl_SubgroupInvocationID, 0, 0);
}
