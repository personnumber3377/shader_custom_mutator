precision mediump float;
precision mediump int;

varying vec4 color;

void main()
{
  const float M_PI = 3.141592653589793;
  vec2 v1;
  vec2 v2 = normalize(vec2(1.0, 1.0));
  float theta = ((color.g * 2.0) * M_PI);
  float phi = ((color.b * 2.0) * M_PI);
  v1.x = (cos(theta) * sin(phi));
  v1.y = (sin(theta) * sin(phi));
  gl_FragColor = vec4(((faceforward(v1, v2, v1) + 1.0) / 2.0), 0.0, 1.0);
}

