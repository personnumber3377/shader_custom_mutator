precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	const float min_c = 0.5;
	float c = color.r;
	if(c > min_c) c = min_c;
	gl_FragColor = vec4(c, 0.0, 0.0, 1.0);
}
