precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	vec4 al = color;
	vec2 m = al.ar;
	vec2 n = al.bg;
	vec4 a = vec4(m.g, n.g, n.r, m.r);
	gl_FragColor = a;
}
