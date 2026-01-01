precision mediump float;
precision mediump int;

attribute vec4 gtf_Vertex;
attribute vec4 gtf_Color;
uniform mat4 gtf_ModelViewProjectionMatrix;
varying vec4 color;
void main ()
{
	const float M_PI = 3.14159265358979323846;
	vec2 c = 2.0 * (gtf_Color.rg - 0.5);
	vec2 asin_c = vec2(0.0);
	vec2 scale = vec2(1.0);
	vec2 sign = vec2(1.0);
	if(c.r < 0.0)
	{
		sign.r = -1.0;
		c.r *= -1.0;
	}
	for(int i = 1; i < 1000; i += 2)
	{
		asin_c.r += scale.r * pow(c.r, float(i)) / float(i);
		scale.r *= float(i) / float(i + 1);
	}
	if(c.g < 0.0)
	{
		sign.g = -1.0;
		c.g *= -1.0;
	}
	for(int i = 1; i < 1000; i += 2)
	{
		asin_c.g += scale.g * pow(c.g, float(i)) / float(i);
		scale.g *= float(i) / float(i + 1);
	}
	color = vec4(sign * asin_c / M_PI + 0.5, 0.0, 1.0);
	gl_Position = gtf_ModelViewProjectionMatrix * gtf_Vertex;
}
