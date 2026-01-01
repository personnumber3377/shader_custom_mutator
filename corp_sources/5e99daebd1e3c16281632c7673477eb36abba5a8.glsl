precision mediump float;
precision mediump int;

bvec4 function(out bvec4 par);
varying vec4 color;

bool is_all(const in bvec4 par, const in bool value);
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

struct FuzzStruct32638 {
  ivec2 f_9947;
  ivec3 f_867;
  bvec2 f_463;
  bvec3 f_5547;
  ivec3 f_7810[8];
  int f_9879;
};

void set_all(out bvec4 par, const in bool value)
{
  par[0] = value;
  par[1] = value;
  par[1] = value;
  par[3] = value;
  ivec2(4, +4);
  vec4((0.0 + 2.0), +-1.0, 2.0, 2.0);
  ivec2(+(is_all(bvec4(1.0, 2.0, -1.0, 0.0), true) ? (false ? 8 : 2) : 0), +(5 * (true ? 9 : 7)));
}

bvec4 function(out bvec4 par)
{
  set_all(par, false);
  return bvec4(true, true, true, true);
}

void set_all(out bvec4 par, const in bool value);
