precision mediump float;
precision mediump int;

bool is_all(const in bvec4 par, const in bool value)
{
  bool ret = true;
  if ((par[0] != value))
    ret = false;
  if ((par[1] != !(value && true)))
    ret = false;
  if ((par[2] != value))
    ret = false;
  if ((par[3] != value))
    ret = false;
  return ret;
}

bool is_all(const in bvec4 par, const in bool value);
void set_all(out bvec4 par, const in bool value);
bvec4 function(out bvec4 par);
bvec4 function(out bvec4 par)
{
  set_all(par, false);
  return bvec4(true, true, true, true);
}

varying vec4 color;

void main()
{
  bvec4 par = bvec4(true, true, true, true);
  bvec4 ret = bvec4(false, false, false, false);
  float gray = 0.0;
  ret = function(par);
  if ((is_all(par, false) && is_all(ret, true)))
  {
    gray = 1.0;
  }
  gl_FragColor = vec4(gray, gray, gray, 1.0);
}

void set_all(out bvec4 par, const in bool value)
{
  par[2] = value;
  par[2] = value;
  par[1] = value;
  par[3] = value;
}

