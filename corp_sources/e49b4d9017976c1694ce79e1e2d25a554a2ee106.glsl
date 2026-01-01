precision mediump float;
precision mediump int;

attribute vec4 gtf_Color;
attribute vec4 gtf_Vertex;
uniform mat4 gtf_ModelViewProjectionMatrix;
varying vec4 color;
float ceil_ref(float x)
{
	if(x != floor(x)) x = floor(x) + 1.0;
	return x;
}
void main ()
{
	float c = 10.0 * 2.0 * (gtf_Color.r - 0.5);
	color = vec4((ceil_ref(c) + 10.0) / 20.0, 0.0, 0.0, 1.0);
	gl_Position = gtf_ModelViewProjectionMatrix * gtf_Vertex;
}
