precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	vec4 al = color;
	vec3 m = al.xyz;
	float k = m.z;
	vec2 n = m.xy;
	vec4 a = vec4(n, k, al.w);
	gl_FragColor = a;
}
