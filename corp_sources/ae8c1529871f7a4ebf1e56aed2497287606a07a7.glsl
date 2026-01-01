precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	float c = color.r;
	gl_FragColor = vec4(1.0 / pow(2.0, 5.0 * c), 0.0, 0.0, 1.0);
}
