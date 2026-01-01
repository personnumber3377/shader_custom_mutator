precision mediump float;
precision mediump int;

attribute vec4 gtf_Color;
attribute vec4 gtf_Vertex;
uniform mat4 gtf_ModelViewProjectionMatrix;
varying vec4 color;
void main ()
{
	vec3 c = 2.0 * (gtf_Color.rgb - 0.5);
	color = vec4(c * sign(c), 1.0);
	gl_Position = gtf_ModelViewProjectionMatrix * gtf_Vertex;
}
