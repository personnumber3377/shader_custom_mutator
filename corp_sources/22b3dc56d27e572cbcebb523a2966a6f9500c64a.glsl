precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
float function(float par[3]);
bool is_all(const in float array[3], const in float value);
void set_all(out float array[3], const in float value);
void main ()
{
	float par[3];
	float ret = 0.0;
	float gray = 0.0;
	set_all(par, 1.0);
	ret = function(par);
	if(is_all(par, 1.0) && (ret == 1.0))
	{
		gray = 1.0;
	}
	gl_FragColor = vec4(gray, gray, gray, 1.0);
}
float function(float par[3])
{
	if(is_all(par, 1.0))
	{
		set_all(par, 0.0);
		return 1.0;
	}
	else
		return 0.0;
}
bool is_all(const in float array[3], const in float value)
{
	bool ret = true;
	if(array[0] != value)
		ret = false;
	if(array[1] != value)
		ret = false;
	if(array[2] != value)
		ret = false;
	return ret;
}
void set_all(out float array[3], const in float value)
{
	array[0] = value;
	array[1] = value;
	array[2] = value;
}
