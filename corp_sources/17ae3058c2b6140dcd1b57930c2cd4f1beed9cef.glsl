precision mediump float;
precision mediump int;

varying vec4 color;

ivec4 function(ivec4 par[3]);
bool is_all(const in ivec4 par, const in int value);
bool is_all(const in ivec4 array[3], const in ivec4 value);
void set_all(out ivec4 array[3], const in ivec4 value);
void main()
{
  ivec4 par[3];
  ivec4 ret = ivec4(0, 0, 0, 0);
  float gray = 0.0;
  set_all(par, ivec4(1, 1, 1, 1));
  ret = function(par);
  if ((is_all(par, ivec4(1, 1, 1, 1)) && is_all(ret, 1)))
  {
    gray = 1.0;
  }
  gl_FragColor = vec4(gray, gray, gray, 1.0);
}

ivec4 function(ivec4 par[3])
{
  if (is_all(par, ivec4(1, 1, 1, 1)))
  {
    set_all(par, ivec4(0, 0, 0, 0));
    return ivec4(1, 1, 1, 1);
  }
  else
    return ivec4(0, 0, 0, 0);
}

bool is_all(const in ivec4 par, const in int value)
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

bool is_all(const in ivec4 array[3], const in ivec4 value)
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

void set_all(out ivec4 array[3], const in ivec4 value)
{
  array[0] = value;
  array[1] = value;
  array[2] = value;
  ivec2((9 - +6), -3);
}

