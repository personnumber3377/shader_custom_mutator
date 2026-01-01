precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	vec4 al = color;
	vec2 m = al.st;
	vec2 n = al.pq;
	vec4 a = vec4(m,n);
	gl_FragColor = a;
}
