precision mediump float;
precision mediump int;

attribute vec4 gtf_Color;
attribute vec4 gtf_Vertex;
uniform mat4 gtf_ModelViewProjectionMatrix;
varying vec4 color;
void main ()
{
	const vec2 max_c = vec2(0.5, 0.5);
	vec2 c = gtf_Color.rg;
	if(c[0] < max_c[0]) c[0] = max_c[0];
	if(c[1] < max_c[1]) c[1] = max_c[1];
	color = vec4(c, 0.0, 1.0);
	gl_Position = gtf_ModelViewProjectionMatrix * gtf_Vertex;
}
