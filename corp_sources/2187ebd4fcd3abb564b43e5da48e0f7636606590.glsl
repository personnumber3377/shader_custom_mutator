precision mediump float;
precision mediump int;

attribute vec4 gtf_Vertex;
uniform mat4 gtf_ModelViewProjectionMatrix;
varying vec4 color;
struct sabcd
{
 mat2 a;
};
void main ()
{
	sabcd s = sabcd(mat2(12.0, 29.0, 13.0, 26.0) );
	color = vec4( vec3(  (s.a[0][0] + s.a[0][1] + s.a[1][0] + s.a[1][1]) / 80.0  ), 1.0);
	gl_Position = gtf_ModelViewProjectionMatrix * gtf_Vertex;
}
