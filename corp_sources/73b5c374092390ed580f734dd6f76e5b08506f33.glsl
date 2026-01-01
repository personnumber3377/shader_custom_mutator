precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	const vec3 y = vec3(0.5, 0.5, 0.5);
	const vec3 a = vec3(0.5, 0.5, 0.5);
	vec3 c = color.rgb;
	gl_FragColor = vec4(c * (1.0 - a) + y * a, 1.0);
}
