precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	vec4 al = color;
	vec2 m = al.zx;
	vec2 n = al.wy;
	vec4 a = vec4(m.y, n.y, m.x, n.x);
	gl_FragColor = a;
}
