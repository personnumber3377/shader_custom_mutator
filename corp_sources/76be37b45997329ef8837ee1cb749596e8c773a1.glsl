precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	vec4 al = color;
	vec2 m = al.br;
	vec2 n = al.ag;
	vec4 a = vec4(m.g, n.g, m.r, n.r);
	gl_FragColor = a;
}
