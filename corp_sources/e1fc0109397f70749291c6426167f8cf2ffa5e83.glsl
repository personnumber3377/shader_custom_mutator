precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	vec4 al = color;
	vec3 m = al.rgb;
	float k = m.b;
	vec2 n = m.rg;
	vec4 a = vec4(n, k, al.a);
	gl_FragColor = a;
}
