precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	const vec3 max_c = vec3(0.5, 0.5, 0.5);
	vec3 c = color.rgb;
	gl_FragColor = vec4(max(c, max_c), 1.0);
}
