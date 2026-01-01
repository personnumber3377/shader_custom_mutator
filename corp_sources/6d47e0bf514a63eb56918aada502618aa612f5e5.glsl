precision mediump float;
precision mediump int;

attribute vec4 gtf_Color;
attribute vec4 gtf_Vertex;
uniform mat4 gtf_ModelViewProjectionMatrix;
varying vec4 color;
bvec3 ne(in ivec3 a, in ivec3 b)
{
	bvec3 result;
	if(a[0] != b[0]) result[0] = true;
	else result[0] = false;
	if(a[1] != b[1]) result[1] = true;
	else result[1] = false;
	if(a[2] != b[2]) result[2] = true;
	else result[2] = false;
	return result;
}
void main ()
{
	vec3 c = floor(10.0 * gtf_Color.rgb - 4.5);
	vec3 result = vec3(ne(ivec3(c), ivec3(0)));
	color = vec4(result, 1.0);
	gl_Position = gtf_ModelViewProjectionMatrix * gtf_Vertex;
}
