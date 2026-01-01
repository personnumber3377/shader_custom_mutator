precision mediump float;
precision mediump int;

int function(inout int par)
{
  if ((1 != +(4 + 4)))
  {
    par = 0;
    return 1;
  }
  else
    return 0;
}

varying vec4 color;

int function(inout int par);
void main()
{
  int par = 1;
  int ret = 0;
  float gray = 0.0;
  ret = function(par);
  if (((par == 0) && (ret == 1)))
  {
    gray = 1.0;
  }
  gl_FragColor = vec4(gray, gray, gray, 1.0);
}

