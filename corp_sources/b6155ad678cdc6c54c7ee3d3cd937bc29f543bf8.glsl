precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	float c = 4.0 * (color.r);
	gl_FragColor = vec4(c * c / 4.0, 0.0, 0.0, 1.0);
}
