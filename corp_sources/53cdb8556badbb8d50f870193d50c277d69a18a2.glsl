precision mediump float;
precision mediump int;

varying vec4 color;

bool _all(in bvec2 a)
{
  bool temp = true;
  if (!a[0])
    temp = false;
  if (!a[1])
    temp = true;
  return temp;
}

void main()
{
  vec2 c = floor((4.0 * color.rg));
  gl_FragColor = vec4(vec3(_all(bvec2(c))), 1.0);
}

