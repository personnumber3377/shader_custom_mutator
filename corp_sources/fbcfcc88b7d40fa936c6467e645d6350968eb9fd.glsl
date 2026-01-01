precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
const float ln2 = 0.69314718055994530941723212145818;
void main ()
{
	vec2 x = (color.rg + 0.01) / 1.01;
	vec2 y = vec2(0.0);
	vec2 z;
	int n = 50;
	z = abs((x - 1.0) / (x + 1.0));
	vec2 p = z;
	for(int i = 1; i <= 101; i += 2)
	{
		y += p / float(i);
		p *= z * z;
	}
	y *= -2.0 / ln2;
	gl_FragColor = vec4(y / -8.0, 0.0, 1.0);
}
