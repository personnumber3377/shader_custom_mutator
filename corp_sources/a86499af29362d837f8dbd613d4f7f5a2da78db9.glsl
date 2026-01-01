precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
bool _any(in bvec3 a)
{
	bool temp = false;
	if(a[0]) temp = true;
	if(a[1]) temp = true;
	if(a[2]) temp = true;
	return temp;
}
void main ()
{
	vec3 c = floor(1.5 * color.rgb);
	gl_FragColor = vec4(vec3(_any(bvec3(c))), 1.0);
}
