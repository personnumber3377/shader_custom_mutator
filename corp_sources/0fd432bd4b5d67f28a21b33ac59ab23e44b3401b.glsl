precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
bvec4 function(inout bvec4 par[10]);
bool is_all(const in bvec4 par, const in bool value);
bool is_all(const in bvec4 array[10], const in bvec4 value);
void set_all(out bvec4 array[10], const in bvec4 value);
void main ()
{
	bvec4 par[10];
	bvec4 ret = bvec4(false, false, false, false);
	float gray = 0.0;
	set_all(par, bvec4(true, true, true, true));
	ret = function(par);
	if(is_all(par, bvec4(false, false, false, false)) && is_all(ret, true))
	{
		gray = 1.0;
	}
	gl_FragColor = vec4(gray, gray, gray, 1.0);
}
bvec4 function(inout bvec4 par[10])
{
	if(is_all(par, bvec4(true, true, true, true)))
	{
		set_all(par, bvec4(false, false, false, false));
		return bvec4(true, true, true, true);
	}
	else
		return bvec4(false, false, false, false);
}
bool is_all(const in bvec4 par, const in bool value)
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
bool is_all(const in bvec4 array[10], const in bvec4 value)
{
	bool ret = true;
	if(array[0] != value)
		ret = false;
	if(array[1] != value)
		ret = false;
	if(array[2] != value)
		ret = false;
	if(array[3] != value)
		ret = false;
	if(array[4] != value)
		ret = false;
	if(array[5] != value)
		ret = false;
	if(array[6] != value)
		ret = false;
	if(array[7] != value)
		ret = false;
	if(array[8] != value)
		ret = false;
	if(array[9] != value)
		ret = false;
	return ret;
}
void set_all(out bvec4 array[10], const in bvec4 value)
{
	array[0] = value;
	array[1] = value;
	array[2] = value;
	array[3] = value;
	array[4] = value;
	array[5] = value;
	array[6] = value;
	array[7] = value;
	array[8] = value;
	array[9] = value;
}
