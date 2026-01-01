precision mediump float;
precision mediump int;

struct FuzzStruct67833 {
  ivec3 f_7323;
  vec4 f_5045;
  bool f_3173;
  bvec4 f_3949;
  mat3 f_192[3];
};

struct sabcd {
  float a;
  float b;
  float c;
  float d;
};

void main()
{
  sabcd s = sabcd(1.0, 2.0, 4.0, 8.0);
  sabcd s2 = sabcd(0.0, 0.0, 0.0, 0.0);
  s2 = s;
  gl_FragColor = vec4(((((s.a + s.b) + s.c) + s.d) / 15.0), ((((s2.a + s2.b) + s2.c) + s2.d) / 15.0), 1.0, 1.0);
  ivec2(1, s.a);
}

