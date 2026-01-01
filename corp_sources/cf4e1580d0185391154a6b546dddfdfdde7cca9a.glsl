precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	vec4 al = color;
	vec3 m = al.arb;
	float g = al.g;
	vec4 a = vec4(m.g, g, m.b, m.r);
	gl_FragColor = a;
}
