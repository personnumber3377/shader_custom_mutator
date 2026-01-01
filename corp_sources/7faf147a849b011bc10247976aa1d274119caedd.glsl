precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	vec4 al = color;
	float s = al.s;
	float t = al.t;
	float p = al.p;
	float q = al.q;
	vec4 m = vec4(s,t,p,q);
	gl_FragColor = m;
}
