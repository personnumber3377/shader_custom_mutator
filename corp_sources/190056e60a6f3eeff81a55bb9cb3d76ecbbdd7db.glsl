precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	vec4 al = color;
	vec3 m = al.rgb;
	float k = m.g;
	vec2 n = m.rb;
	vec4 a = vec4(n.r, k, n.g, al.a);
	gl_FragColor = a;
}
