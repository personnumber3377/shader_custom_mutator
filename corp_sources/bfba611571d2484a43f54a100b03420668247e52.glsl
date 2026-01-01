precision mediump float;
precision mediump int;

attribute vec4 gtf_Vertex;
attribute vec4 gtf_Color;
uniform mat4 gtf_ModelViewProjectionMatrix;
varying vec4 color;
void main ()
{
	color = gtf_Color;
	gl_PointSize = 20.0;
	gl_Position = gtf_ModelViewProjectionMatrix * gtf_Vertex;
}
