precision mediump float;
precision mediump int;

attribute vec4 gtf_Vertex;
uniform mat4 gtf_ModelViewProjectionMatrix;
varying vec2 vertXY;
void main ()
{
	vertXY = gtf_Vertex.xy;
	gl_Position = gtf_ModelViewProjectionMatrix * gtf_Vertex;
}
