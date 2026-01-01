precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	const vec2 edge = vec2(0.5, 0.5);
	vec2 c = color.rg;
	if(c[0] >= edge[0])
	{
		c[0] = 1.0;
	}
	else
	{
		c[0] = 0.0;
	}
	if(c[1] >= edge[1])
	{
		c[1] = 1.0;
	}
	else
	{
		c[1] = 0.0;
	}
	gl_FragColor = vec4(c, 0.0, 1.0);
}
