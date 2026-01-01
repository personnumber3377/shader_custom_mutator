precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	float c = sqrt(100.0 * color.r);
	gl_FragColor = vec4(c * c / 100.0, 0.0, 0.0, 1.0);
}
