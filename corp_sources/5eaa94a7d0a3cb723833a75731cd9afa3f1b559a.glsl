precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	float c = (color.r * 99.0) + 1.0;
	gl_FragColor = vec4(1.0 / sqrt(c), 0.0, 0.0, 1.0);
}
