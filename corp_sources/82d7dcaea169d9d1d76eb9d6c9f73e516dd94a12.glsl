precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	const vec3 edge = vec3(0.5, 0.5, 0.5);
	gl_FragColor = vec4(step(edge, color.rgb), 1.0);
}
