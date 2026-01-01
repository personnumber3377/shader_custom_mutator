precision mediump float;
precision mediump int;

precision mediump float;
precision mediump float;
varying vec4 color;
void main ()
{
	const float M_PI = 3.14159265358979323846;
	float x = 2.0 * (color.g - 0.5);
	float y = 2.0 * (color.b - 0.5);
	const float epsilon = 1.0e-4;
	gl_FragColor = vec4(0.0, 0.0, 0.0, 1.0);
	if(x > epsilon || abs(y) > epsilon)
	{
		gl_FragColor = vec4(atan(y, x) / (2.0 * M_PI) + 0.5, 0.0, 0.0, 1.0);
	}
}
