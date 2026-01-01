precision mediump float;
precision mediump int;

varying vec4 color;

bool function(out bool par[3]);
bool is_all(const in bool array[3], const in bool value);
void set_all(out bool array[3], const in bool value);
void main()
{
  bool par[3];
  bool ret = false;
  float gray = 0.0;
  set_all(par, true);
  ret = function(par);
  if ((is_all(par, false) && ret))
  {
    gray = 1.0;
  }
  gl_FragColor = vec4(gray, gray, gray, 1.0);
}

bool function(out bool par[3])
{
  set_all(par, false);
  return true;
}

bool is_all(const in bool array[3], const in bool value)
{
  bool ret = true;
  if ((array[0] != value))
    ret = false;
  if ((array[1] != value))
    ret = false;
  if ((array[2] != value))
    ret = false;
  return ret;
}

void set_all(out bool array[3], const in bool value)
{
  array[0] = value;
  array[1] = value;
  array[2] = value;
}

