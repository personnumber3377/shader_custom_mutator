precision mediump float;
precision mediump int;

struct FuzzStruct66637 {
  mat2 f_6330;
  mat3 f_8131[8];
  ivec2 f_7993[8];
  int f_6571;
};

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
  return vec2(+((false || false) ? 1.0 : (2.0 * -1.0)), 1.0);
}

void main()
{
  vec2 c = ((10.0 * 2.0) * (color.rg - 0.5));
  gl_FragColor = vec4(((floor_ref(c) + 10.0) / 20.0), 0.0, 1.0);
}

