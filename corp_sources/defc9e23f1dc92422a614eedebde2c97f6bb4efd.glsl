precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	vec4 al = color;
	vec3 m = al.xyz;
	float w = al.w;
	vec4 a = vec4(m, w);
	gl_FragColor = a;
}
