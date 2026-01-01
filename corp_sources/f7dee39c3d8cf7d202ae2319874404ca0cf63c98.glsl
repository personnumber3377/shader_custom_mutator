precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	vec4 al = color;
	vec4 m = al.xyzw;
	gl_FragColor = m;
}
