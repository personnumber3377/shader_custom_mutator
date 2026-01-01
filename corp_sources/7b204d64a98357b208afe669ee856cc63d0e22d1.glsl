precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
int function(int par);
void main ()
{
	int par = 1;
	int ret = 0;
	float gray = 0.0;
	ret = function(par);
	if((par == 1) && (ret == 1))
	{
		gray = 1.0;
	}
	gl_FragColor = vec4(gray, gray, gray, 1.0);
}
int function(int par)
{
	if(par == 1)
	{
		par = 0;
		return 1;
	}
	else
		return 0;
}
