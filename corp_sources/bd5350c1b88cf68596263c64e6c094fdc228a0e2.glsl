precision mediump float;
precision mediump int;

attribute vec4 gtf_Vertex;
uniform mat4 gtf_ModelViewProjectionMatrix;
varying vec4 position;
void main()
{
	gl_Position = gtf_ModelViewProjectionMatrix * gtf_Vertex;
	position = gl_Position;
}
