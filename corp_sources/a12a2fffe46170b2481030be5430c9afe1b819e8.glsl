precision mediump float;
precision mediump int;

attribute vec4 gtf_Color;
attribute vec4 gtf_Vertex;
uniform mat4 gtf_ModelViewProjectionMatrix;
varying vec4 color;
void main ()
{
	const float M_PI = 3.14159265358979323846;
	float v1 = (gtf_Color.g * 2.0) - 1.0;
	float v2 = (gtf_Color.b * 2.0) - 1.0;
	if(dot(v1, v2) >= 0.0) v1 *= -1.0;
	color = vec4((v1 + 1.0) / 2.0, 0.0, 0.0, 1.0);
	gl_Position = gtf_ModelViewProjectionMatrix * gtf_Vertex;
}
