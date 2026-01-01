precision mediump float;
precision mediump int;

attribute vec4 gtf_Color;
attribute vec4 gtf_Vertex;
uniform mat4 gtf_ModelViewProjectionMatrix;
varying vec4 color;
void main ()
{
	vec4 lightloc = gtf_Vertex;
	vec3 m = lightloc.xyz;
	vec3 t = m.zyx;
	vec4 a = vec4(t.z, t.y, t.x, lightloc.w);
	color = gtf_Color;
	gl_Position = gtf_ModelViewProjectionMatrix * a;
}
