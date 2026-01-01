precision mediump float;
precision mediump int;

attribute vec4 gtf_Vertex;
attribute vec4 gtf_Color;
uniform mat4 gtf_ModelViewProjectionMatrix;
varying vec4 color;
void main ()
{
	const float M_PI = 3.14159265358979323846;
	float x = 2.0 * (gtf_Color.g - 0.5);
	float y = 2.0 * (gtf_Color.b - 0.5);
	const float epsilon = 1.0e-4;
	color = vec4(0.0, 0.0, 0.0, 1.0);
	if(x > epsilon || abs(y) > epsilon)
	{
		color = vec4(atan(y, x) / (2.0 * M_PI) + 0.5, 0.0, 0.0, 1.0);
	}
	gl_Position = gtf_ModelViewProjectionMatrix * gtf_Vertex;
}
