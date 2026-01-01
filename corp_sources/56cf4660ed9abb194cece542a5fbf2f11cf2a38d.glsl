precision mediump float;
precision mediump int;

attribute vec4 gtf_Vertex;
uniform mat4 gtf_ModelViewProjectionMatrix;
varying vec4 color;
float gray = 0.0;
void function();
void main ()
{
	gray = 0.0;
	function();
	color = vec4(gray, gray, gray, 1.0);
	gl_Position = gtf_ModelViewProjectionMatrix * gtf_Vertex;
}
void function()
{
	gray = 1.0;
}
