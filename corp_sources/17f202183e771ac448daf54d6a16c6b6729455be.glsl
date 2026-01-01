precision mediump float;
precision mediump int;

attribute vec4 gtf_Vertex;
attribute float gtf_PointSize;
uniform mat4 gtf_ModelViewProjectionMatrix;
void main ()
{
	gl_Position = gtf_ModelViewProjectionMatrix * gtf_Vertex;
	gl_PointSize = gtf_PointSize;
}
