precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	vec2 c = -color.rg;
	gl_FragColor = vec4(exp(3.0 * c), 0.0, 1.0);
}
