precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	const float y = 0.5;
	const float a = 0.5;
	float c = color.r;
	gl_FragColor = vec4(mix(c, y, a), 0.0, 0.0, 1.0);
}
