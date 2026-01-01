precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	vec4 al = color;
	vec3 m = al.stp;
	float k = m.p;
	vec2 n = m.st;
	vec4 a = vec4(n, k, al.q);
	gl_FragColor = a;
}
