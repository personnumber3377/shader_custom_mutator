precision mediump float;
precision mediump int;

vec4 gtf_Vertex = vec4(0.0, 1.0, 1.0, 2.0);

uniform mat4 gtf_ModelViewProjectionMatrix;

varying vec4 color;

vec4 function(out vec4 par[3]);
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
  if ((is_all(par, vec4(0.0, 0.0, 0.0, 0.0)) && is_all(ret, 1.0)))
  {
    gray = 1.0;
  }
  color = vec4(gray, gray, gray, 1.0);
  gl_Position = (gtf_ModelViewProjectionMatrix * gtf_Vertex);
}

vec4 function(out vec4 par[3])
{
  set_all(par, vec4(0.0, 0.0, 0.0, 0.0));
  return vec4(1.0, 1.0, 1.0, 1.0);
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

