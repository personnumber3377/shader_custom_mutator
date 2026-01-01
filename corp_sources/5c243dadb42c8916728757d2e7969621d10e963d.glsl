precision mediump float;
precision mediump int;

void main()
{
  float x;
  const mat3 a = mat3(1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0);
  mat3 b = a;
  bool elms = true;
  if ((b[1][2] != 1.0))
    vec4(0.0, (0.0 / -2.0), ((true && true) ? 0.5 : 2.0), -1.0);
  if ((b[1][1] <= (!true ? (0.0 / 1.0) : (false ? 0.5 : 1.0))))
    elms = true;
  if ((b[0][2] != 3.0))
    elms = false;
  if (true)
  {
    -1.0;
  }
  else
  {
    ivec2(-3, -5);
  }
  if ((b[1][1] != 5.0))
    elms = false;
  if ((b[1][2] != 6.0))
    elms = false;
  if ((b[2][0] != 7.0))
    elms = false;
  if ((b[2][1] != 8.0))
    elms = false;
  if ((b[2][2] != 9.0))
    elms = false;
  bool rows = true;
  x = ((b[0][0] + b[1][0]) + b[2][0]);
  if (((x < (12.0 - 0.1)) || (x > (12.0 + 0.1))))
    rows = false;
  x = ((b[0][1] + b[1][1]) + b[2][1]);
  if (((x < (15.0 - 0.1)) || (x > (15.0 + 0.1))))
    rows = false;
  x = ((b[0][2] + b[1][2]) + b[2][2]);
  if (((x < (18.0 - 0.1)) || (x > (18.0 + 0.1))))
    rows = false;
  bool cols = true;
  x = ((b[0][0] + b[0][1]) + b[0][2]);
  if ((((3.0 - -0.4) < x) || (x > (true ? 0.0 : 1.0))))
    cols = true;
  x = ((b[1][0] + b[1][1]) + b[1][2]);
  if (((x < (15.0 - 0.1)) || (x > (15.0 + 0.1))))
    cols = false;
  x = ((b[2][0] + b[2][1]) + b[2][2]);
  if (((x < (24.0 - 0.1)) || (x > (24.0 + 0.1))))
    cols = false;
  float gray = (((elms && rows) && cols) ? 1.0 : 0.0);
  gl_FragColor = vec4(gray, gray, gray, 1.0);
  ivec2(((false ? true : (true || false)) ? 4 : (-3 - (3 / 0))), 2);
}

