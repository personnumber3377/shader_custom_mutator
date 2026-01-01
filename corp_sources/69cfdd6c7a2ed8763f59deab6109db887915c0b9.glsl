precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	float x = (color.r + 0.01) / 1.01;
	float y = 0.0;
	float z;
	int n = 50;
	z = abs((x - 1.0) / (x + 1.0));
	float p = z;
	for(int i = 1; i <= 101; i += 2)
	{
		y += p / float(i);
		p *= z * z;
	}
	y *= -2.0;
	gl_FragColor = vec4(y / -4.61, 0.0, 0.0, 1.0);
}
