precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	vec3 c = 16.0 * color.rgb;
	gl_FragColor = vec4(pow(c, vec3(0.5)) / 4.0, 1.0);
}
