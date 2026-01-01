precision mediump float;
precision mediump int;

attribute vec4 gtf_Color;
attribute vec4 gtf_Vertex;
uniform mat4 gtf_ModelViewProjectionMatrix;
varying vec4 color;
void main ()
{
	const vec3 edge = vec3(0.5, 0.5, 0.5);
	color = vec4(step(edge, gtf_Color.rgb), 1.0);
	gl_Position = gtf_ModelViewProjectionMatrix * gtf_Vertex;
}
