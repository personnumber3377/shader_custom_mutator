precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	vec4 al = color;
	vec4 m = al.qspt;
	vec4 a = vec4(m.t, m.q, m.p, m.s);
	gl_FragColor = a;
}
