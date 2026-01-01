precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main()
{
	gl_FragColor = vec4((434.0 / 500.0) * (color.gb - 0.5) + 0.5, 0.0, 1.0);
}
