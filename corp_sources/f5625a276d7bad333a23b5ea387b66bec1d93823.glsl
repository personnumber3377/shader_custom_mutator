precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
int function(inout int par[3]);
bool is_all(const in int array[3], const in int value);
void set_all(out int array[3], const in int value);
void main ()
{
	int par[3];
	int ret = 0;
	float gray = 0.0;
	set_all(par, 1);
	ret = function(par);
	if(is_all(par, 0) && (ret == 1))
	{
		gray = 1.0;
	}
	gl_FragColor = vec4(gray, gray, gray, 1.0);
}
int function(inout int par[3])
{
	if(is_all(par, 1))
	{
		set_all(par, 0);
		return 1;
	}
	else
		return 0;
}
bool is_all(const in int array[3], const in int value)
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
void set_all(out int array[3], const in int value)
{
	array[0] = value;
	array[1] = value;
	array[2] = value;
}
