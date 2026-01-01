precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	vec3 c = 2.0 * (color.rgb - 0.5);
	gl_FragColor = vec4(exp2(2.0 * c) / 4.0, 1.0);
}
