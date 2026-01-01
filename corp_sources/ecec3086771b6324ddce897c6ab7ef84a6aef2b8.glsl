precision mediump float;
precision mediump int;

attribute vec4 gtf_Color;
attribute vec4 gtf_Vertex;
uniform mat4 gtf_ModelViewProjectionMatrix;
varying vec4 color;
void main ()
{
	const float min_c = 0.25;
	const float max_c = 0.75;
	float c = gtf_Color.r;
	if(c > max_c) c = max_c;
	if(c < min_c) c = min_c;
	color = vec4(c, 0.0, 0.0, 1.0);
	gl_Position = gtf_ModelViewProjectionMatrix * gtf_Vertex;
}
