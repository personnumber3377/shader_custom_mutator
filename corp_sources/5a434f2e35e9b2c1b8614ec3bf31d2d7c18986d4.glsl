precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	vec2 c = 4.0 * (color.rg);
	gl_FragColor = vec4(c * c / 4.0, 0.0, 1.0);
}
