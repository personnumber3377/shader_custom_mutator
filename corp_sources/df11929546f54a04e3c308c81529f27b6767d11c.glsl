precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
const mat4 mat_ones = mat4(1.0, 1.0, 1.0, 1.0,
			   1.0, 1.0, 1.0, 1.0,
			   1.0, 1.0, 1.0, 1.0,
			   1.0, 1.0, 1.0, 1.0);
const mat4 mat_zeros = mat4(0.0, 0.0, 0.0, 0.0,
			    0.0, 0.0, 0.0, 0.0,
			    0.0, 0.0, 0.0, 0.0,
			    0.0, 0.0, 0.0, 0.0);
mat4 function(inout mat4 par[2]);
bool is_all(const in mat4 par, const in float value);
bool is_all(const in mat4 array[2], const in mat4 value);
void set_all(out mat4 array[2], const in mat4 value);
void main ()
{
	mat4 par[2];
	mat4 ret = mat_zeros;
	float gray = 0.0;
	set_all(par, mat_ones);
	ret = function(par);
	if(is_all(par, mat_zeros) && is_all(ret, 1.0))
	{
		gray = 1.0;
	}
	gl_FragColor = vec4(gray, gray, gray, 1.0);
}
mat4 function(inout mat4 par[2])
{
	if(is_all(par, mat_ones))
	{
		set_all(par, mat_zeros);
		return mat_ones;
	}
	else
		return mat_zeros;
}
bool is_all(const in mat4 par, const in float value)
{
	bool ret = true;
	if(par[0][0] != value)
		ret = false;
	if(par[0][1] != value)
		ret = false;
	if(par[0][2] != value)
		ret = false;
	if(par[0][3] != value)
		ret = false;
	if(par[1][0] != value)
		ret = false;
	if(par[1][1] != value)
		ret = false;
	if(par[1][2] != value)
		ret = false;
	if(par[1][3] != value)
		ret = false;
	if(par[2][0] != value)
		ret = false;
	if(par[2][1] != value)
		ret = false;
	if(par[2][2] != value)
		ret = false;
	if(par[2][3] != value)
		ret = false;
	if(par[3][0] != value)
		ret = false;
	if(par[3][1] != value)
		ret = false;
	if(par[3][2] != value)
		ret = false;
	if(par[3][3] != value)
		ret = false;
	return ret;
}
bool is_all(const in mat4 array[2], const in mat4 value)
{
	bool ret = true;
	if(array[0] != value)
		ret = false;
	if(array[1] != value)
		ret = false;
	return ret;
}
void set_all(out mat4 array[2], const in mat4 value)
{
	array[0] = value;
	array[1] = value;
}
