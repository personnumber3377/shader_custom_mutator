precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	const float M_PI = 3.14159265358979323846;
	vec2 c = 2.0 * M_PI * 2.0 * (color.rg - 0.5);
	gl_FragColor = vec4(degrees(c) / (2.0 * 360.0) + 0.5, 0.0, 1.0);
}
