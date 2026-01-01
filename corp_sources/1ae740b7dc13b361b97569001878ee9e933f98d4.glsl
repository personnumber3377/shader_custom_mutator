precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	vec3 c = 10.0 * 2.0 * (color.rgb - 0.5);
	c = abs(fract(c) - 0.5) * 2.0;
	gl_FragColor = vec4(c, 1.0);
}
