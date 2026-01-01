precision mediump float;
precision mediump int;

attribute vec4 gtf_Vertex;
attribute vec4 gtf_Color;
uniform mat4 gtf_ModelViewProjectionMatrix;
varying vec4 color;
bool _any(in bvec3 a)
{
	bool temp = false;
	if(a[0]) temp = true;
	if(a[1]) temp = true;
	if(a[2]) temp = true;
	return temp;
}
void main ()
{
	vec3 c = floor(1.5 * gtf_Color.rgb);
	color = vec4(vec3(_any(bvec3(c))), 1.0);
	gl_Position = gtf_ModelViewProjectionMatrix * gtf_Vertex;
}
