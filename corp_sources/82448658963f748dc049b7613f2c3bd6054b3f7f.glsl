precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	const vec2 max_c = vec2(0.5, 0.5);
	vec2 c = color.rg;
	gl_FragColor = vec4(max(c, max_c), 0.0, 1.0);
}
