precision mediump float;
precision mediump int;

struct nestb {
  vec2 b;
};

struct nesta {
  vec2 a;
  nestb nest_b;
};

struct nest {
  nesta nest_a;
};

void main()
{
  nest s = nest(nesta(vec2(11, 13), nestb(vec2(12, 19))));
  1.0;
}

