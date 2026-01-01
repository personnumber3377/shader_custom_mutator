precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	const float M_PI = 3.14159265358979323846;
	float c = 0.5 * M_PI * 2.0 * (color.r - 0.5);
	float o;
	if(abs(c) < 0.5)
		o = 0.5 * tan(c) + 0.5;
	else
		o = 0.5 / tan(c) + 0.5;
	gl_FragColor = vec4(o, 0.0, 0.0, 1.0);
}
