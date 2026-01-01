precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	vec4 al = color;
	vec4 m = al.barg;
	vec4 a = vec4(m.b, m.a, m.r, m.g);
	gl_FragColor = a;
}
