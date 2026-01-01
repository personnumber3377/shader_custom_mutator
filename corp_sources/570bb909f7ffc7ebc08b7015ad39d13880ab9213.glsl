precision mediump float;
precision mediump int;

void set_all(out bvec4 par, const in bool value);
bvec4 function(out bvec4 par)
{
  set_all(par, false);
  return bvec4(true, true, true, true);
}

bool is_all(const in bvec4 par, const in bool value);
varying vec4 color;

void set_all(out bvec4 par, const in bool value)
{
  par[0] = value;
  par[1] = is_all(bvec4(-1.0, (0.0 + +1.0), 0.0, ((true || true) ? (false ? 2.0 : (true ? 0.0 : 1.0)) : (true ? 0.0 : 0.0))), (false && false));
  par[1] = value;
  par[3] = value;
  ivec2(8, -1);
}

bool is_all(const in bvec4 par, const in bool value)
{
  bool ret = true;
  if ((par[0] != value))
    ret = false;
  if ((par[1] != value))
    ret = false;
  if ((par[2] != value))
    ret = false;
  if ((par[3] != value))
    ret = false;
  return ret;
}

bvec4 function(out bvec4 par);
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

