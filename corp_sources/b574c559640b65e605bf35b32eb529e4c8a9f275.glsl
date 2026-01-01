precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	float c = color.r;
	gl_FragColor = vec4(exp2(5.0 * c) / 32.0, 0.0, 0.0, 1.0);
}
