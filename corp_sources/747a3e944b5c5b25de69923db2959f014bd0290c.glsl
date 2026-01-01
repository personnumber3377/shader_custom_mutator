precision mediump float;
precision mediump int;

struct sabcd {
  vec3 a;
  vec3 b;
};

void main()
{
  sabcd s = sabcd(vec3(12.0, 29.0, 32.0), vec3(13.0, 26.0, 38.0));
  gl_FragColor = vec4(vec3(((((((s.a[0] + s.a[1]) + s.a[2]) + s.b[0]) + s.b[1]) + s.b[2]) / 150.0)), 1.0);
}

