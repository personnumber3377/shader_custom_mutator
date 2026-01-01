precision mediump float;
precision mediump int;

varying vec4 color;

int function(out int par);
void main()
{
  int par = 1;
  int ret = -2;
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

