precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	const float exp1 = 2.7183;
	vec2 c = color.rg;
	gl_FragColor = vec4(1.0 / pow(vec2(exp1), 3.0 * c), 0.0, 1.0);
}
