precision mediump float;
precision mediump int;

attribute vec4 gtf_Color;
attribute vec4 gtf_Vertex;
uniform mat4 gtf_ModelViewProjectionMatrix;
varying vec4 color;
void main ()
{
	const float M_PI = 3.14159265358979323846;
	vec2 c = 0.5 * M_PI * 2.0 * (gtf_Color.rg - 0.5);
	vec2 o;
	if(abs(c.r) < 0.5)
		o.r = 0.5 * tan(c.r) + 0.5;
	else
		o.r = 0.5 / tan(c.r) + 0.5;
	if(abs(c.g) < 0.5)
		o.g = 0.5 * tan(c.g) + 0.5;
	else
		o.g = 0.5 / tan(c.g) + 0.5;
	color = vec4(o, 0.0, 1.0);
	gl_Position = gtf_ModelViewProjectionMatrix * gtf_Vertex;
}
