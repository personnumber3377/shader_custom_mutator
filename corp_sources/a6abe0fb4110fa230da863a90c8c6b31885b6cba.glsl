precision mediump float;
precision mediump int;

attribute vec4 gtf_Vertex;
uniform mat4 gtf_ModelViewProjectionMatrix;
varying vec4 color;
struct nestb
{
	vec2 b;
};
struct nesta
{
	vec2 a;
	nestb nest_b;
};
struct nest
{
	nesta nest_a;
};
void main ()
{
	nest s = nest(nesta(vec2(11, 13), nestb(vec2(12, 19) ) ) );
	color = vec4( vec3(  (s.nest_a.a[0] + s.nest_a.a[1] + s.nest_a.nest_b.b[0] + s.nest_a.nest_b.b[1] ) / 55.0 ), 1.0);
	gl_Position = gtf_ModelViewProjectionMatrix * gtf_Vertex;
}
