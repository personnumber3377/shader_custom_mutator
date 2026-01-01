precision mediump float;
precision mediump int;

varying vec4 color;

vec2 ceil_ref(vec2 x)
{
  if ((x[0] != floor(x[0])))
    x[0] = (floor(x[0]) + 1.0);
  if ((x[1] != floor(x[1])))
    x[1] = (floor(x[1]) + 1.0);
  return x;
}

void main()
{
  vec2 c = ((10.0 * 2.0) * (color.rg - 0.5));
  gl_FragColor = vec4(((ceil_ref(c) + 10.0) / 20.0), 0.0, 1.0);
  ivec2(5, 8);
}

