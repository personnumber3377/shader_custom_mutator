precision mediump float;
precision mediump int;

precision mediump float;
struct nestb
{
	vec3 b;
};
struct nesta
{
	vec3 a;
	nestb nest_b;
};
struct nest
{
	nesta nest_a;
};
void main ()
{
	nest s = nest(nesta(vec3(11, 13, 17), nestb(vec3(12, 19, 29) ) ) );
	gl_FragColor = vec4( vec3(  (s.nest_a.a[0] + s.nest_a.a[1] + s.nest_a.a[2] + s.nest_a.nest_b.b[0] + s.nest_a.nest_b.b[1] + s.nest_a.nest_b.b[2]) / 101.0 ), 1.0);
}
