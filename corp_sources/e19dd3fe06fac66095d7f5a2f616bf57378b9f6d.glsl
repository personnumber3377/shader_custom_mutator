precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	vec3 c = 2.0 * (color.rgb - 0.5);
	gl_FragColor = vec4(c * (sign(c)), 1.0);
}
