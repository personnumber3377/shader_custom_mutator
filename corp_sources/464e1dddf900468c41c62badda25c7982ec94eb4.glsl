precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
float function(float par);
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
	gl_FragColor = vec4(gray, gray, gray, 1.0);
}
float function(float par)
{
	if(par == 1.0)
	{
		par = 0.0;
		return 1.0;
	}
	else
		return 0.0;
}
