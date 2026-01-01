precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	const vec2 edge = vec2(0.5, 0.5);
	gl_FragColor = vec4(step(edge, color.rg), 0.0, 1.0);
}
