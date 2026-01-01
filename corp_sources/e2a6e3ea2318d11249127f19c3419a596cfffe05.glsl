precision mediump float;
precision mediump int;

attribute vec4 gtf_Vertex;
uniform mat4 gtf_ModelViewProjectionMatrix;
varying vec4 color;
bool function(in bool par);
void main ()
{
	bool par = true;
	bool ret = false;
	float gray = 0.0;
	ret = function(par);
	if(par && ret)
	{
		gray = 1.0;
	}
	color = vec4(gray, gray, gray, 1.0);
	gl_Position = gtf_ModelViewProjectionMatrix * gtf_Vertex;
}
bool function(in bool par)
{
	if(par)
	{
		par = false;
		return true;
	}
	else
		return false;
}
