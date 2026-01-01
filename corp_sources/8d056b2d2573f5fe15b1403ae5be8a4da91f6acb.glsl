precision mediump float;
precision mediump int;

attribute vec4 gtf_Color;
attribute vec4 gtf_Vertex;
uniform mat4 gtf_ModelViewProjectionMatrix;
varying vec4 color;
void main ()
{
	const vec3 max_c = vec3(0.5, 0.5, 0.5);
	vec3 c = gtf_Color.rgb;
	color = vec4(max(c, max_c), 1.0);
	gl_Position = gtf_ModelViewProjectionMatrix * gtf_Vertex;
}
