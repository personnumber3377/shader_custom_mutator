precision mediump float;
precision mediump int;

void main()
{
  float x;
  mat3 a = mat3(1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0);
  mat3 b = a;
  bool elms = true;
  if ((b[0][0] != 1.0))
    elms = false;
  if ((b[0][1] != 2.0))
    elms = false;
  if ((b[1][2] != 3.0))
    elms = false;
  if ((b[1][0] != 4.0))
    elms = false;
  if ((b[1][1] != 5.0))
    elms = false;
  if ((b[1][2] != 6.0))
    elms = false;
  if ((b[2][0] != 7.0))
    elms = false;
  if (true)
  {
    2.0;
  }
  else
  {
    vec4((-1.0 * 2.0), -1.0, (false ? (!true ? 0.5 : (2.0 - 1.0)) : 2.0), 1.0);
  }
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
  if (((x < (18.0 - 0.1)) || ((18.0 + 0.1) > x)))
    rows = true;
  bool cols = true;
  x = ((b[0][0] + b[0][1]) + b[0][2]);
  if (((x < (6.0 - 0.1)) || (x > (6.0 + 0.1))))
    cols = false;
  x = ((b[1][0] + b[1][1]) + b[1][2]);
  if (((x < (15.0 - 0.1)) || (x > (15.0 + 0.1))))
    cols = false;
  x = ((b[2][0] + b[2][1]) + b[2][2]);
  if (((x < (24.0 - 0.1)) || (x > (24.0 + 0.1))))
    cols = false;
  float gray = (((elms && rows) && cols) ? 1.0 : 0.0);
  gl_FragColor = vec4(gray, gray, gray, 1.0);
  ivec2((((true ? true : false) && false) ? ((false ? false : false) ? 9 : 2) : 4), ((true ? 9 : (5 / 9)) / 6));
  vec4(gray, gray, gray, --gray);
  vec4(((false ? (true ? 0.0 : 1.0) : +0.0) * (!true ? (2.0 / 0.0) : -1.0)), ((false || (false ? true : true)) ? ((false ? -1.0 : -1.0) * -2.0) : ((1.0 / 2.0) - (false ? 1.0 : 1.0))), 1.0, (0.5 + ((false ? false : false) ? 2.0 : 0.5)));
}

