precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
bool _any(in bvec2 a)
{
	bool temp = false;
	if(a[0]) temp = true;
	if(a[1]) temp = true;
	return temp;
}
void main ()
{
	vec2 c = floor(1.5 * color.rg);
	gl_FragColor = vec4(vec3(_any(bvec2(c))), 1.0);
}
