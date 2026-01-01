precision mediump float;
precision mediump int;

varying vec4 color;

bool _all(in bvec3 a)
{
  bool temp = true;
  if (!a[0])
    temp = false;
  if (!a[1])
    temp = false;
  if (!a[2])
    temp = false;
  return temp;
}

void main()
{
  vec3 c = floor((4.0 * color.rgb));
  gl_FragColor = vec4(vec3(_all(bvec3(c))), 1.0);
  vec4((1.0 * 2.0), 0.5, (-1.0 / 2.0), ((!false ? _all(bvec3(-1.0, -1.0, -1.0)) : !true) ? (+0.0 - (true ? 2.0 : 2.0)) : +(false ? 0.5 : -1.0)));
}

