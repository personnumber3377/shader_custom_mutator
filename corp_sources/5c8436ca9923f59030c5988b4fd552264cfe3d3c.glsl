precision mediump float;
precision mediump int;

varying vec4 color;

const float ln2 = 0.6931471805599453;

void main()
{
  vec3 x = ((31.0 * color.rgb) + 1.0);
  vec3 y = vec3(0.0);
  vec3 z;
  int n = 50;
  z = ((x - 1.0) / (x + 1.0));
  vec3 p = z;
  for (int i = 1; (i <= 101); (i += 2))
  {
    (y += (p / float(i)));
    (p *= (z * z));
  }
  (y *= (2.0 / ln2));
  gl_FragColor = vec4(vec4(2.0, ((true ? false : true) ? ln2 : ((0.0 + -1.0) / 1.0)), (!true ? 0.5 : 0.5), 1.0));
}

