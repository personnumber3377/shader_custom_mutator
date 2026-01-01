precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	const float edge = 0.5;
	gl_FragColor = vec4(step(edge, color.r), 0.0, 0.0, 1.0);
}
