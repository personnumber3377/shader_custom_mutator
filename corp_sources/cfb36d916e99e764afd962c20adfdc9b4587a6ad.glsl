precision mediump float;
precision mediump int;

attribute vec4 gtf_Color;
attribute vec4 gtf_Vertex;
uniform mat4 gtf_ModelViewProjectionMatrix;
varying vec4 color;
void main ()
{
	const float M_PI = 3.14159265358979323846;
	float c = 0.5 * M_PI * 2.0 * (gtf_Color.r - 0.5);
	float o;
	if(abs(c) < 0.5)
		o = 0.5 * (sin(c) / cos(c)) + 0.5;
	else
		o = 0.5 * (cos(c) / sin(c)) + 0.5;
	color = vec4(o, 0.0, 0.0, 1.0);
	gl_Position = gtf_ModelViewProjectionMatrix * gtf_Vertex;
}
