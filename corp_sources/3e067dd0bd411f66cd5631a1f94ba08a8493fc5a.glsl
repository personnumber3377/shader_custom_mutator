precision mediump float;
precision mediump int;

attribute vec4 gtf_Vertex;
uniform mat4 gtf_ModelViewProjectionMatrix;
varying vec4 color;
int function(out int par[3]);
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
	color = vec4(gray, gray, gray, 1.0);
	gl_Position = gtf_ModelViewProjectionMatrix * gtf_Vertex;
}
int function(out int par[3])
{
	set_all(par, 0);
	return 1;
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
