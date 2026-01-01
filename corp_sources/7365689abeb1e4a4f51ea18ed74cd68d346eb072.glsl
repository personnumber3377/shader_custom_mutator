precision mediump float;
precision mediump int;

attribute vec4 gtf_Color;
attribute vec4 gtf_Vertex;
uniform mat4 gtf_ModelViewProjectionMatrix;
varying vec4 color;
void main ()
{
	float c = 2.0 * (gtf_Color.r - 0.5);
	if(c > 0.0) c = 1.0 * c;
	if(c < 0.0) c = -1.0 * c;
	color = vec4(c, 0.0, 0.0, 1.0);
	gl_Position = gtf_ModelViewProjectionMatrix * gtf_Vertex;
}
