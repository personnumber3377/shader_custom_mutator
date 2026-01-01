precision mediump float;
precision mediump int;

attribute vec4 gtf_Color;
attribute vec4 gtf_Vertex;
uniform mat4 gtf_ModelViewProjectionMatrix;
varying vec4 color;
vec2 ceil_ref(vec2 x)
{
	if(x[0] != floor(x[0])) x[0] = floor(x[0]) + 1.0;
	if(x[1] != floor(x[1])) x[1] = floor(x[1]) + 1.0;
	return x;
}
void main ()
{
	vec2 c = 10.0 * 2.0 * (gtf_Color.rg - 0.5);
	color = vec4((ceil_ref(c) + 10.0) / 20.0, 0.0, 1.0);
	gl_Position = gtf_ModelViewProjectionMatrix * gtf_Vertex;
}
