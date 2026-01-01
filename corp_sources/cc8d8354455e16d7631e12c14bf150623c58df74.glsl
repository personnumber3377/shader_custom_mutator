precision mediump float;
precision mediump int;

struct FuzzStruct79113 {
  bvec3 f_878;
  vec3 f_8837;
  mat4 f_3330;
};

varying vec4 color;

vec4 function(in vec4 par[3]);
bool is_all(const in vec4 par, const in float value);
bool is_all(const in vec4 array[3], const in vec4 value);
void set_all(out vec4 array[3], const in vec4 value);
void main()
{
  vec4 par[3];
  vec4 ret = vec4(0.0, 0.0, 0.0, 0.0);
  float gray = 0.0;
  set_all(par, vec4(1.0, 1.0, 1.0, 1.0));
  ret = function(par);
  if ((is_all(par, vec4(1.0, 1.0, 1.0, 1.0)) && is_all(ret, 1.0)))
  {
    gray = 1.0;
  }
  gl_FragColor = vec4(gray, gray, gray, 1.0);
}

vec4 function(in vec4 par[3])
{
  if (is_all(par, vec4(1.0, 1.0, 1.0, 1.0)))
  {
    set_all(par, vec4(0.0, 0.0, 0.0, 0.0));
    return vec4(1.0, 1.0, 1.0, 1.0);
  }
  else
    return vec4(0.0, 0.0, 0.0, 0.0);
}

bool is_all(const in vec4 par, const in float value)
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

bool is_all(const in vec4 array[3], const in vec4 value)
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

void set_all(out vec4 array[3], const in vec4 value)
{
  array[0] = value;
  array[1] = value;
  array[2] = value;
}

