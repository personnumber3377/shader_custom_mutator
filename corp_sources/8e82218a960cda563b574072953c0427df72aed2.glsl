precision mediump float;
precision mediump int;

varying vec4 color;

vec2 floor_ref(vec2 x)
{
  if ((x[0] >= 0.0))
    x[0] = float(int(x[0]));
  else
    x[0] = float((int(x[0]) - 1));
  if ((x[1] >= 0.0))
    x[1] = float(int(x[1]));
  else
    x[1] = float((int(x[1]) - 1));
  return x;
}

void main()
{
  vec2 c = (0.5 * (0.5 - color.rg));
  gl_FragColor = vec4(((floor_ref(c) + 10.0) / 20.0), 0.0, 1.0);
}

