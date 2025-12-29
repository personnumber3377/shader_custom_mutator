layout(location = 0) flat in int instanceIndex;
layout(depth_less) out float gl_FragDepth;
void main()
{
  gl_FragDepth = float(instanceIndex) / float(81);
}
