precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	const float M_PI = 3.14159265358979323846;
	float v1 = (color.g + 1.0) / 2.0;
	float v2 = (color.b + 1.0) / 2.0;
	gl_FragColor = vec4((reflect(v1, v2) + 1.0) / 2.0, 0.0, 0.0, 1.0);
}
