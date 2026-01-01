precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	vec2 c = 31.0 * color.rg + 1.0;
	gl_FragColor = vec4(log2(c) / 5.0, 0.0, 1.0);
}
