precision mediump float;
precision mediump int;

precision mediump float;
struct nestb
{
	float b;
};
struct nesta
{
	float a;
	nestb nest_b;
};
struct nest
{
	nesta nest_a;
};
void main ()
{
	nest s = nest(nesta(1.0, nestb(2.0)));
	gl_FragColor = vec4(vec3((s.nest_a.a + s.nest_a.nest_b.b) / 3.0), 1.0);
}
