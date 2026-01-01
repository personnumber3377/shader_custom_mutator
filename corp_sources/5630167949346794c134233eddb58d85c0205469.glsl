precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	vec4 al = color;
	vec3 m = al.rgb;
	float a = al.a;
	vec4 b = vec4(m, a);
	gl_FragColor = b;
}
