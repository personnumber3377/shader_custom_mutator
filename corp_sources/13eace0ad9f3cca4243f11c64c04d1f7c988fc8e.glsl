precision mediump float;
precision mediump int;

attribute vec4 gtf_Vertex;
uniform mat4 gtf_ModelViewProjectionMatrix;
varying vec4 color;
int function(out int par);
void main ()
{
	int par = 1;
	int ret = 0;
	float gray = 0.0;
	ret = function(par);
	if((par == 0) && (ret == 1))
	{
		gray = 1.0;
	}
	color = vec4(gray, gray, gray, 1.0);
	gl_Position = gtf_ModelViewProjectionMatrix * gtf_Vertex;
}
int function(out int par)
{
	par = 0;
	return 1;
}
