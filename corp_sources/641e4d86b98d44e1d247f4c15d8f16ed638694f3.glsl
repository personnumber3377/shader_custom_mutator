precision mediump float;
precision mediump int;

struct FuzzStruct71770 {
  vec3 f_8467[2];
  int f_839;
  bvec4 f_6737;
  bvec4 f_6687;
  vec4 f_6701;
  bvec3 f_7480;
};

varying vec4 color;

void main()
{
  const float M_PI = 3.141592653589793;
  vec3 v1;
  vec3 v2 = vec3(1.0, 0.0, 0.0);
  float theta = ((color.g * 2.0) * M_PI);
  float phi = ((color.b * 2.0) * M_PI);
  v1.x = (cos(theta) * sin(phi));
  v1.y = (sin(theta) * sin(phi));
  v1.z = cos(phi);
  gl_FragColor = vec4(((cross(v1, v2) + 1.0) / 2.0), 1.0);
}

