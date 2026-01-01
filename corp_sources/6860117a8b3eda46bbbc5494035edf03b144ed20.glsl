precision mediump float;
precision mediump int;

attribute vec4 gtf_Color;
attribute vec4 gtf_Vertex;
uniform mat4 gtf_ModelViewProjectionMatrix;
varying vec4 color;
void main ()
{
	color = vec4(vec3(sqrt(gtf_Color.r*gtf_Color.r + gtf_Color.g*gtf_Color.g + gtf_Color.b*gtf_Color.b) / 3.0), 1.0);
	gl_Position = gtf_ModelViewProjectionMatrix * gtf_Vertex;
}
