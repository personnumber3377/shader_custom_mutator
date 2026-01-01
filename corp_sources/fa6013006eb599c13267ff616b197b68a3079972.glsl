precision mediump float;
precision mediump int;

varying vec4 color;

float floor_ref(float x)
{
  if ((x >= 0.0))
    x = float(int(x));
  else
    x = float((int(x) - 1));
  return x;
}

void main()
{
  float c = ((10.0 * 2.0) * (color.r - 0.5));
  gl_FragColor = vec4(((floor_ref(c) + 10.0) / 20.0), 0.0, 0.0, 1.0);
  vec4((0.0 * 1.0), 2.0, floor_ref(floor_ref(floor_ref(c))), (2.0 * (false ? -1.0 : 1.0)));
}

