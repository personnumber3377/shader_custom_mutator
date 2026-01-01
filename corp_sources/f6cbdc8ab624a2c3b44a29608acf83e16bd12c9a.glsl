precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
float ceil_ref(float x)
{
	if(x != floor(x)) x = floor(x) + 1.0;
	return x;
}
void main ()
{
	float c = 10.0 * 2.0 * (color.r - 0.5);
	gl_FragColor = vec4((ceil_ref(c) + 10.0) / 20.0, 0.0, 0.0, 1.0);
}
