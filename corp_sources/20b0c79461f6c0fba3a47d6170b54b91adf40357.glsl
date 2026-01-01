precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
bool function(bool par);
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
	gl_FragColor = vec4(gray, gray, gray, 1.0);
}
bool function(bool par)
{
	if(par)
	{
		par = false;
		return true;
	}
	else
		return false;
}
