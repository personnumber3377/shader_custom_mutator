precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	const float min_c = 0.25;
	const float max_c = 0.75;
	float c = color.r;
	if(c > max_c) c = max_c;
	if(c < min_c) c = min_c;
	gl_FragColor = vec4(c, 0.0, 0.0, 1.0);
}
