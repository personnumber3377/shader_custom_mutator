precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	vec4 al = color;
	vec3 m = al.rgb;
	float k = m.r;
	vec2 n = m.gb;
	vec4 a = vec4(k, n.r, n.g, al.a);
	gl_FragColor = a;
}
