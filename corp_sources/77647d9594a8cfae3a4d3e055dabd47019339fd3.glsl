precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	const float M_PI = 3.14159265358979323846;
	vec2 x = 2.0 * (color.gg - 0.5);
	vec2 y = 2.0 * (color.bb - 0.5);
	const float epsilon = 1.0e-4;
	gl_FragColor = vec4(0.0, 0.0, 0.0, 1.0);
	if(x[0] > epsilon || abs(y[0]) > epsilon)
	{
		gl_FragColor[0] = atan(y[0], x[0]) / (2.0 * M_PI) + 0.5;
	}
	if(x[1] > epsilon || abs(y[1]) > epsilon)
	{
		gl_FragColor[1] = atan(y[1], x[1]) / (2.0 * M_PI) + 0.5;
	}
}
