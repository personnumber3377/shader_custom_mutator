precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	vec2 c = 2.0 * (color.rg - 0.5);
	gl_FragColor = vec4(c * sign(c), 0.0, 1.0);
}
