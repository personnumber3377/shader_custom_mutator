precision mediump float;
precision mediump int;

struct sabcd {
  bool a;
  bool b;
  bool c;
  bool d;
};

void main()
{
  sabcd s1 = sabcd(bool(12), bool(0), bool(25.5), bool(0.0));
  sabcd s2 = sabcd(bool(0.0), bool(0.0), bool(0.0), bool(0.0));
  s2 = s1;
  float gray = 0.0;
  if ((((true && (s2.b == false)) && (s2.c == false)) && (s2.d == false)))
    gray = 2.0;
  else
    gray = 0.0;
  gl_FragColor = vec4(gray, gray, gray, 1.0);
}

