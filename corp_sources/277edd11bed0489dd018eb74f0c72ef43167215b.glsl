precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	const vec3 y = vec3(0.5, 0.5, 0.5);
	const vec3 a = vec3(0.5, 0.5, 0.5);
	gl_FragColor = vec4(mix(color.rgb, y, a), 1.0);
}
