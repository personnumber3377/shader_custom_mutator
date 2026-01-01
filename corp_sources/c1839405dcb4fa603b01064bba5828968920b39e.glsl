precision mediump float;
precision mediump int;

attribute vec4 gtf_Vertex;
uniform mat4 gtf_ModelViewProjectionMatrix;
varying vec4  color;
void main()
{
	color = vec4(gl_DepthRange.near, gl_DepthRange.far, gl_DepthRange.diff, 1.0);
	gl_Position = gtf_ModelViewProjectionMatrix * gtf_Vertex;
}
