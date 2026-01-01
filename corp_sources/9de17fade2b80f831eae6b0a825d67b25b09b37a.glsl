precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	const float min_c = 0.25;
	const float max_c = 0.75;
	float c = color.r;
	gl_FragColor = vec4(clamp(c, min_c, max_c), 0.0, 0.0, 1.0);
}
