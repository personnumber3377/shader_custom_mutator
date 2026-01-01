precision mediump float;
precision mediump int;

uniform vec3 a[8];

uniform bool ub;

varying mat4 vm;

int foo(float None);
float bar(int i)
{
  return float(i);
}

void main()
{
  const int x = 3;
  mat4 a[4];
  vec4 v = vec4((+0.0 - bar(4)), (false ? 0.5 : 2.0), -(-1.0 / (false ? 0.0 : 1.0)), 0.5);
  for (float f = 0.0; (f != 3.0); ++f)
  {
  }
  vec3 v3[(x + x)];
  int vi = foo(2.3);
  vec3 v3_1 = v3[x];
  float f1 = (a[x][2].z * float(x));
  f1 = (a[x][2][2] * float(x));
  f1 = (v[2] * v[1]);
  const int ci = 2;
}

int foo(float f)
{
  return 2;
}

