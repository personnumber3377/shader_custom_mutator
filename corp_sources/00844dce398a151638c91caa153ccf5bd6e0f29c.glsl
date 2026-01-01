precision mediump float;
precision mediump int;

attribute vec4 gtf_Color;
attribute vec4 gtf_Vertex;
uniform mat4 gtf_ModelViewProjectionMatrix;
varying vec4 color;
void main ()
{
	vec4 lightloc = gtf_Vertex;
	vec2 m = lightloc.ar;
	vec2 n = lightloc.bg;
	vec4 a = vec4(m.g, n.g, n.r, m.r);
	color = gtf_Color;
	gl_Position = gtf_ModelViewProjectionMatrix * a;
}
