precision mediump float;
precision mediump int;

vec4 gtf_Vertex = vec4(2.0, 0.0, -1.0, -0.0);

uniform mat4 gtf_ModelViewProjectionMatrix;

varying vec4 color;

bvec4 function(in bvec4 par[3]);
bool is_all(const in bvec4 par, const in bool value);
bool is_all(const in bvec4 array[3], const in bvec4 value);
void set_all(out bvec4 array[3], const in bvec4 value);
void main()
{
  bvec4 par[3];
  bvec4 ret = bvec4(false, false, false, false);
  float gray = 0.0;
  set_all(par, bvec4(true, true, true, true));
  ret = function(par);
  if ((is_all(par, bvec4(true, true, true, true)) && is_all(ret, true)))
  {
    gray = 1.0;
  }
  color = vec4(gray, gray, gray, 1.0);
  gl_Position = (gtf_ModelViewProjectionMatrix * gtf_Vertex);
}

bvec4 function(in bvec4 par[3])
{
  if (is_all(par, bvec4(true, true, true, true)))
  {
    set_all(par, bvec4(false, false, false, false));
    return bvec4(true, true, true, true);
  }
  else
    return bvec4(false, false, false, false);
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

bool is_all(const in bvec4 array[3], const in bvec4 value)
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

void set_all(out bvec4 array[3], const in bvec4 value)
{
  array[0] = value;
  array[1] = value;
  array[2] = value;
}

