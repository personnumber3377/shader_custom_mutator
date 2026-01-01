precision mediump float;
precision mediump int;

attribute vec4 gtf_Color;
attribute vec4 gtf_Vertex;
uniform mat4 gtf_ModelViewProjectionMatrix;
varying vec4 color;
bvec2 gt(in vec2 a, in vec2 b)
{
	bvec2 result;
	if(a[0] > b[0]) result[0] = true;
	else result[0] = false;
	if(a[1] > b[1]) result[1] = true;
	else result[1] = false;
	return result;
}
void main ()
{
	vec2 c = floor(10.0 * gtf_Color.rg - 4.5);
	vec2 result = vec2(gt(c, vec2(0.0)));
	color = vec4(result, 0.0, 1.0);
	gl_Position = gtf_ModelViewProjectionMatrix * gtf_Vertex;
}
