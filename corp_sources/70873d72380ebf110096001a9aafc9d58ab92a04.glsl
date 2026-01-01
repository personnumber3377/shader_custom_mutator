precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	float c = (color.r + 0.01) / 1.01;
	gl_FragColor = vec4(log2(c) / -8.0, 0.0, 0.0, 1.0);
}
