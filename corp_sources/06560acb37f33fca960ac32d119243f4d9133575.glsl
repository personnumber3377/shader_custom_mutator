precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	vec2 x = 31.0 * color.rg + 1.0;
	vec2 y = vec2(0.0);
	vec2 z;
	int n = 50;
	z = (x - 1.0) / (x + 1.0);
	vec2 p = z;
	for(int i = 1; i <= 101; i += 2)
	{
		y += p / float(i);
		p *= z * z;
	}
	y *= 2.0;
	gl_FragColor = vec4(y / 3.466, 0.0, 1.0);
}
