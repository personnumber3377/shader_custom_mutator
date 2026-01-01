precision mediump float;
precision mediump int;

attribute vec4 gtf_Vertex;
uniform mat4 gtf_ModelViewProjectionMatrix;
varying vec4 color;
float function(in float par);
void main ()
{
	float par = 1.0;
	float ret = 0.0;
	float gray = 0.0;
	ret = function(par);
	if((par == 1.0) && (ret == 1.0))
	{
		gray = 1.0;
	}
	color = vec4(gray, gray, gray, 1.0);
	gl_Position = gtf_ModelViewProjectionMatrix * gtf_Vertex;
}
float function(in float par)
{
	if(par == 1.0)
	{
		par = 0.0;
		return 1.0;
	}
	else
		return 0.0;
}
