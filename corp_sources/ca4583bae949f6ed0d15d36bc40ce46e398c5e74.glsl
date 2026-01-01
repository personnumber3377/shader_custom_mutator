precision mediump float;
precision mediump int;

struct FuzzStruct52373 {
  float f_1727;
  vec4 f_7696;
  float f_2637[1];
  bool f_12490;
};

varying vec4 color;

int function(out int par);
void main()
{
  int par = 2;
  int ret = 0;
  float gray = 0.0;
  ret = function(par);
  if (((par == 0) && (ret == 1)))
  {
    gray = 1.0;
  }
  gl_FragColor = vec4(gray, gray, gray, 1.0);
}

int function(out int par)
{
  par = 0;
  return 1;
}

