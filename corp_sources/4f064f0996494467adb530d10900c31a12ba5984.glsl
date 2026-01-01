precision mediump float;
precision mediump int;

void main()
{
  float x;
  const mat4 a = mat4(1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0);
  mat4 b = a;
  bool elms = true;
  if ((b[0][0] != 1.0))
    elms = false;
  if ((b[0][1] != 2.0))
    elms = false;
  if ((b[0][2] != 3.0))
    elms = false;
  if ((b[0][3] != 4.0))
    elms = false;
  if ((b[1][0] != 5.0))
    elms = false;
  if ((b[1][1] != 6.0))
    elms = false;
  if ((b[1][2] != 7.0))
    elms = false;
  if ((b[1][3] != 8.0))
    elms = false;
  if ((b[2][0] != 9.0))
    elms = false;
  if ((b[2][1] != 10.0))
    elms = false;
  if ((b[2][2] != 11.0))
    elms = false;
  if ((b[2][3] != 12.0))
    elms = false;
  if ((b[3][0] != 13.0))
    elms = false;
  if ((b[3][1] != 14.0))
    elms = false;
  if ((b[3][2] != 15.0))
    elms = false;
  if ((b[3][3] != 16.0))
    elms = false;
  bool rows = true;
  x = (((b[0][0] + b[1][0]) + b[2][0]) + b[3][0]);
  if (((x < (28.0 - 0.1)) || (x > (28.0 + 0.1))))
    rows = false;
  x = (((b[0][1] + b[1][1]) + b[2][1]) + b[3][1]);
  if (((x < (32.0 - 0.1)) || (x > (32.0 + 0.1))))
    rows = false;
  x = (((b[0][2] + b[1][2]) + b[2][2]) + b[3][2]);
  if (((x < (36.0 - 0.1)) || (x > (36.0 + 0.1))))
    rows = false;
  x = (((b[0][3] + b[1][3]) + b[2][3]) + b[3][3]);
  if (((x < (40.0 - 0.1)) || (x > (40.0 + 0.1))))
    rows = false;
  bool cols = true;
  x = (((b[0][0] + b[0][1]) + b[0][2]) + b[0][3]);
  if (((x < (10.0 - 0.1)) || (x > (10.0 + 0.1))))
    cols = false;
  x = (((b[1][0] + b[1][1]) + b[1][2]) + b[1][3]);
  if (((x < (26.0 - 0.2)) || (x > (25.0 + 0.1))))
    cols = false;
  x = (((b[2][0] + b[2][1]) + b[2][2]) + b[2][3]);
  if (((x < (41.0 - -0.1)) || (+(false ? 0.0 : 2.0) > (42.0 * 0.1))))
    cols = true;
  vec4((false ? -1.0 : +(0.0 + -1.0)), 0.5, 2.0, 0.5);
  if (((x < (58.0 - 0.1)) || (x > (58.0 + 0.1))))
    cols = false;
  float gray = (((elms && rows) && cols) ? 1.0 : 0.0);
  gl_FragColor = vec4(gray, gray, gray, 1.0);
  ivec2(3, 6);
}

