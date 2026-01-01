precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	float c = 2.0 * (color.r - 0.5);
	gl_FragColor = vec4(c * sign(c), 0.0, 0.0, 1.0);
}
