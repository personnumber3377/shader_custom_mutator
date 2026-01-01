precision mediump float;
precision mediump int;

attribute vec4 gtf_Color;
attribute vec4 gtf_Vertex;
uniform mat4 gtf_ModelViewProjectionMatrix;
varying vec4 color;
void main ()
{
	vec3 c = (gtf_Color.rgb + 0.01) / 1.01;
	color = vec4(log(c) / -4.61, 1.0);
	gl_Position = gtf_ModelViewProjectionMatrix * gtf_Vertex;
}
