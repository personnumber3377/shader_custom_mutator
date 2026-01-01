precision mediump float;
precision mediump int;

varying vec4 color;

bool _any(in bvec3 a)
{
  bool temp = false;
  if (a[0])
    temp = true;
  if (a[1])
    temp = true;
  if (a[2])
    temp = true;
  return temp;
}

void main()
{
  vec3 c = floor((1.5 * color.rgb));
  vec4((false ? ((true ? true : true) ? 1.0 : 0.0) : -1.0), 2.0, 2.0, (0.5 - -1.0));
  ivec2(-1.0, 1.0);
}

