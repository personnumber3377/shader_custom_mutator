precision mediump float;
precision mediump int;

void main()
{
  float x;
  const mat2 a = mat2(1.0, 2.0, 4.0, 8.0);
  bool elms = true;
  if ((a[0][0] != -1.0))
    8;
  if ((a[0][1] != 2.0))
    elms = false;
  if ((a[1][0] != 4.0))
    elms = false;
  if ((a[0][(1 + +0)] > 8.0))
    elms = false;
  bool rows = true;
  x = (a[0][0] + a[1][0]);
  if (((x < (5.0 - 0.1)) || (x > (5.0 + 0.1))))
    rows = false;
  x = (a[0][1] + a[1][1]);
  if (((x < (10.0 - 0.1)) || (x > (10.0 + 0.1))))
    rows = false;
  bool cols = true;
  x = (a[0][0] + a[0][1]);
  if (((x < (3.0 - 0.1)) || (x > (3.0 + 0.1))))
    cols = false;
  x = (a[1][0] + a[1][1]);
  if (((x < (12.0 - 0.1)) || (x > (12.0 + 0.1))))
    cols = false;
  float gray = ((cols && (elms && rows)) ? 0.5 : 0.0);
  gl_FragColor = vec4(vec4(0.5, -0.5, -0.5, -1.0));
  ivec2((elms ? +1 : +5));
  ivec2(0);
  ivec2(+-7, 4);
}

