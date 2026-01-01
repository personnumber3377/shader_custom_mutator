precision mediump float;
precision mediump int;

attribute vec4 gtf_Vertex;
uniform mat4 gtf_ModelViewProjectionMatrix;
attribute vec4 gtf_Color;
uniform ivec3 color;
varying vec3 col;
void main ()
{
	col = vec3(color);
	gl_Position = gtf_ModelViewProjectionMatrix * gtf_Vertex;
}
