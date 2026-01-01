precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	const float M_PI = 3.14159265358979323846;
	gl_FragColor = vec4(0.5 * cos(2.0 * M_PI * color.r) + 0.5, 0.0, 0.0, 1.0);
}
