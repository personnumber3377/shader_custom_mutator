precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	const float M_PI = 3.14159265358979323846;
	vec3 c = 360.0 * 2.0 * (color.rgb - 0.5);
	gl_FragColor = vec4((c * M_PI / 180.0) / (4.0 * M_PI) + 0.5, 1.0);
}
