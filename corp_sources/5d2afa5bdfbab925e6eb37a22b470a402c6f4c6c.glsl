precision mediump float;
precision mediump int;

attribute vec4 gtf_Color;
attribute vec4 gtf_Vertex;
uniform mat4 gtf_ModelViewProjectionMatrix;
varying vec4 color;
void main ()
{
	const vec3 y = vec3(0.5, 0.5, 0.5);
	const vec3 a = vec3(0.5, 0.5, 0.5);
	vec3 c = gtf_Color.rgb;
	color = vec4(c * (1.0 - a) + y * a, 1.0);
	gl_Position = gtf_ModelViewProjectionMatrix * gtf_Vertex;
}
