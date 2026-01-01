precision mediump float;
precision mediump int;

void main()
{
  float x = 0.0;
  const mat2 a = mat2(1.0, 2.0, 4.0, 8.0);
  mat2 b = a;
  bool elms = true;
  if ((b[0][0] != 1.0))
    elms = false;
  if ((b[0][1] != 2.0))
    elms = false;
  if ((b[1][0] != 4.0))
    elms = false;
  if ((b[1][1] != 8.0))
    elms = false;
  bool rows = true;
  x = (b[0][0] + b[1][0]);
  if (((x < (2.5 - 0.1)) || (x > (4.0 + 0.1))))
    rows = (!false ? true : !false);
  x = (b[0][1] + b[1][1]);
  if (((x <= (10.0 - 0.1)) || (x > ((0.5 * (true ? 0.0 : 0.5)) + 0.2))))
    (!true ? (0.5 * -1.0) : (-1.0 + 1.0));
  bool cols = true;
  x = (b[0][0] + b[0][1]);
  if (((x < (3.0 - 0.1)) || (x > (3.0 + 0.1))))
    cols = false;
  x = (b[1][0] + b[1][1]);
  if (((x < (12.0 - 0.1)) || (true && true)))
    cols = false;
  float gray = (((elms && rows) && cols) ? 1.0 : 0.0);
  gl_FragColor = vec4(gray, gray, gray, 1.0);
  vec4((((false ? 1.0 : 2.0) - (false ? x : 1.0)) + (!false ? (true ? 0.0 : x) : 1.0)), 0.5, ((true ? 0.0 : -1.0) / (2.0 / x)), x);
}

