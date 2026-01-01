precision mediump float;
precision mediump int;

attribute vec4 gtf_Color;
attribute vec4 gtf_Vertex;
uniform mat4 gtf_ModelViewProjectionMatrix;
varying vec4 color;
void main ()
{
	vec2 c = 10.0 * 2.0 * (gtf_Color.rg - 0.5);
	c = abs((c - floor(c)) - 0.5) * 2.0;
	color = vec4(c, 0.0, 1.0);
	gl_Position = gtf_ModelViewProjectionMatrix * gtf_Vertex;
}
