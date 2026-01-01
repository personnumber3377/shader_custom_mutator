precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	const float exp1 = 2.7183;
	const float exp3 = 20.0855;
	vec3 c = color.rgb;
	gl_FragColor = vec4(pow(vec3(exp1), 3.0 * c) / exp3, 1.0);
}
