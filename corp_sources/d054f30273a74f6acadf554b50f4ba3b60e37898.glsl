precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
vec3 ceil_ref(vec3 x)
{
	if(x[0] != floor(x[0])) x[0] = floor(x[0]) + 1.0;
	if(x[1] != floor(x[1])) x[1] = floor(x[1]) + 1.0;
	if(x[2] != floor(x[2])) x[2] = floor(x[2]) + 1.0;
	return x;
}
void main ()
{
	vec3 c = 10.0 * 2.0 * (color.rgb - 0.5);
	gl_FragColor = vec4((ceil_ref(c) + 10.0) / 20.0, 1.0);
}
