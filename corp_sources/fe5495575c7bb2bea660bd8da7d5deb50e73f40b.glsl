precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	const float M_PI = 3.14159265358979323846;
	vec3 c = 0.5 * M_PI * 2.0 * (color.rgb - 0.5);
	vec3 o;
	if(abs(c.r) < 0.5)
		o.r = 0.5 * tan(c.r) + 0.5;
	else
		o.r = 0.5 / tan(c.r) + 0.5;
	if(abs(c.g) < 0.5)
		o.g = 0.5 * tan(c.g) + 0.5;
	else
		o.g = 0.5 / tan(c.g) + 0.5;
	if(abs(c.b) < 0.5)
		o.b = 0.5 * tan(c.b) + 0.5;
	else
		o.b = 0.5 / tan(c.b) + 0.5;
	gl_FragColor = vec4(o, 1.0);
}
