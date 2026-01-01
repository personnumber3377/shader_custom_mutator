precision mediump float;
precision mediump int;

varying vec4 color;

bool function(bool par);
void main()
{
  bool par = true;
  bool ret = false;
  float gray = 0.0;
  ret = function(par);
  if ((par && ret))
  {
    gray = 1.0;
  }
  gl_FragColor = vec4(gray, gray, gray, 1.0);
}

bool function(bool par)
{
  if (par)
  {
    par = true;
    return true;
  }
  else
    return true;
  ivec2(((true ? 6 : -7) + 6), (((true && par) ? false : !false) ? 8 : 9));
}

