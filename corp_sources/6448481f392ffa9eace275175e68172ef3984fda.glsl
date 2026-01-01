precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	float c = 10.0 * 2.0 * (color.r - 0.5);
	c = abs((c - floor(c)) - 0.5) * 2.0;
	gl_FragColor = vec4(c, 0.0, 0.0, 1.0);
}
