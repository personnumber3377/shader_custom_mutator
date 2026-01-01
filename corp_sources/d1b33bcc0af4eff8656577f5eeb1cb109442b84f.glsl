precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
vec4 function(in vec4 par);
bool is_all(const in vec4 par, const in float value);
void set_all(out vec4 par, const in float value);
void main ()
{
	vec4 par = vec4(1.0, 1.0, 1.0, 1.0);
	vec4 ret = vec4(0.0, 0.0, 0.0, 0.0);
	float gray = 0.0;
	ret = function(par);
	if(is_all(par, 1.0) && is_all(ret, 1.0))
	{
		gray = 1.0;
	}
	gl_FragColor = vec4(gray, gray, gray, 1.0);
}
vec4 function(in vec4 par)
{
	if(is_all(par, 1.0))
	{
		set_all(par, 0.0);
		return vec4(1.0, 1.0, 1.0, 1.0);
	}
	else
		return vec4(0.0, 0.0, 0.0, 0.0);
}
bool is_all(const in vec4 par, const in float value)
{
	bool ret = true;
	if(par[0] != value)
		ret = false;
	if(par[1] != value)
		ret = false;
	if(par[2] != value)
		ret = false;
	if(par[3] != value)
		ret = false;
	return ret;
}
void set_all(out vec4 par, const in float value)
{
	par[0] = value;
	par[1] = value;
	par[2] = value;
	par[3] = value;
}
