precision mediump float;
precision mediump int;

precision mediump float;
precision mediump float;
varying vec4 color;
bvec2 _not(in bvec2 a)
{
	bvec2 result;
	if(a[0]) result[0] = false;
	else result[0] = true;
	if(a[1]) result[1] = false;
	else result[1] = true;
	return result;
}
void main ()
{
	vec2 c = floor(1.5 * color.rg);
	gl_FragColor = vec4(vec2(_not(bvec2(c))), 0.0, 1.0);
}
