precision mediump float;
precision mediump int;

attribute vec4 gtf_Vertex;
uniform mat4 gtf_ModelViewProjectionMatrix;
attribute vec4 gtf_Color;
uniform vec4 color;
varying vec4 col;
void main ()
{
	col = color;
	gl_Position = gtf_ModelViewProjectionMatrix * gtf_Vertex;
}
