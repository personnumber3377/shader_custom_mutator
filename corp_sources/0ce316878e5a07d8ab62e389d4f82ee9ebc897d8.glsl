precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	vec3 c = 16.0 * color.rgb;
	gl_FragColor = vec4(sqrt(c) / 4.0, 1.0);
}
