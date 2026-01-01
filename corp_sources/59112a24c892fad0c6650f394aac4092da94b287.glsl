precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	vec3 x = (color.rgb + 0.01) / 1.01;
	vec3 y = vec3(0.0);
	vec3 z;
	int n = 50;
	z = abs((x - 1.0) / (x + 1.0));
	vec3 p = z;
	for(int i = 1; i <= 101; i += 2)
	{
		y += p / float(i);
		p *= z * z;
	}
	y *= -2.0;
	gl_FragColor = vec4(y / -4.61, 1.0);
}
