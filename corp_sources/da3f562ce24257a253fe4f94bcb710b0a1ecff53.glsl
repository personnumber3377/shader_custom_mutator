precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	const float M_PI = 3.14159265358979323846;
	float c = 2.0 * (color.r - 0.5);
	gl_FragColor = vec4(acos(c) / M_PI, 0.0, 0.0, 1.0);
}
