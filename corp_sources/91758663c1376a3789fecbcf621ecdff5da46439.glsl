precision mediump float;
precision mediump int;

attribute vec4 gtf_Color;
attribute vec4 gtf_Vertex;
uniform mat4 gtf_ModelViewProjectionMatrix;
varying vec4 color;
void main ()
{
	vec4 lightloc = gtf_Vertex;
	vec4 m = lightloc.barg;
	vec4 a = vec4(m.b, m.a, m.r, m.g);
	color = gtf_Color;
	gl_Position = gtf_ModelViewProjectionMatrix * a;
}
