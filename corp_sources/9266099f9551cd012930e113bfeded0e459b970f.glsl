precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	vec2 c = color.rg;
	gl_FragColor = vec4(pow(vec2(2.0), 5.0 * c) / 32.0, 0.0, 1.0);
}
