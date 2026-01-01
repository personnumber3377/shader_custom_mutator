precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	const vec2 y = vec2(0.5, 0.5);
	const vec2 a = vec2(0.5, 0.5);
	gl_FragColor = vec4(mix(color.rg, y, a), 0.0, 1.0);
}
