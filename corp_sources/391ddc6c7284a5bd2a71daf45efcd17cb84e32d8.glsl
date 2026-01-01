precision mediump float;
precision mediump int;

vec4 gtf_Vertex = vec4(2.0, (true ? ((0.5 + 0.5) / 1.0) : +1.0), ((false || (true || true)) ? +(true ? 0.5 : 2.0) : (true ? -0.0 : +1.0)), 0.0);

uniform mat4 gtf_ModelViewProjectionMatrix;

varying vec4 color;

struct nestb {
  float b;
};

struct nesta {
  float a;
  nestb nest_b;
};

struct nest {
  nesta nest_a;
};

void main()
{
  nest s = nest(nesta(1.0, nestb(2.0)));
  color = vec4(vec3(((s.nest_a.a + s.nest_a.nest_b.b) / 3.0)), 1.0);
  gl_Position = (gtf_ModelViewProjectionMatrix * gtf_Vertex);
}

