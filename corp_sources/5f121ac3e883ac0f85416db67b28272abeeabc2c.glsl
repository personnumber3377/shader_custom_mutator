precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	vec4 al = color;
	vec3 m = al.stp;
	vec4 a = vec4(m.stp,al.q);
	gl_FragColor = a;
}
