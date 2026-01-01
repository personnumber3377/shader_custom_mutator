precision mediump float;
precision mediump int;

attribute vec4 gtf_Vertex;
attribute vec4 gtf_Color;
uniform mat4 gtf_ModelViewProjectionMatrix;
varying vec4 color;
void main ()
{
	vec2 c = floor(4.0 * gtf_Color.rg);
	color = vec4(vec3(all(bvec2(c))), 1.0);
	gl_Position = gtf_ModelViewProjectionMatrix * gtf_Vertex;
}
