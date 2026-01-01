precision mediump float;
precision mediump int;

attribute vec4 gtf_Color;
attribute vec4 gtf_Vertex;
uniform mat4 gtf_ModelViewProjectionMatrix;
varying vec4 color;
void main ()
{
	const vec3 edge = vec3(0.5, 0.5, 0.5);
	vec3 c = gtf_Color.rgb;
	if(c[0] >= edge[0])
	{
		c[0] = 1.0;
	}
	else
	{
		c[0] = 0.0;
	}
	if(c[1] >= edge[1])
	{
		c[1] = 1.0;
	}
	else
	{
		c[1] = 0.0;
	}
	if(c[2] >= edge[2])
	{
		c[2] = 1.0;
	}
	else
	{
		c[2] = 0.0;
	}
	color = vec4(c, 1.0);
	gl_Position = gtf_ModelViewProjectionMatrix * gtf_Vertex;
}
