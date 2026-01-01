precision mediump float;
precision mediump int;

struct nestb {
  bool b;
};

struct nesta {
  bool a;
  nestb nest_b;
};

struct nest {
  nesta nest_a;
};

void main()
{
  nest s = nest(nesta(bool(1.0), nestb(bool(0.0))));
  float gray = 0.0;
  if (((s.nest_a.a == true) && (s.nest_a.nest_b.b == false)))
    gray = 1.0;
  else
    gray = 0.0;
  (true ? vec4(-1.0, +(0.5 / (true ? 0.5 : 0.5)), (2.0 + (2.0 - (true ? -1.0 : 2.0))), 0.0) : vec4(2.0, (2.0 + ((-1.0 + 1.0) * 2.0)), 1.0, +(0.5 + (false ? 0.5 : -1.0))));
}

