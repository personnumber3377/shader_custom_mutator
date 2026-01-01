precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	vec3 c = color.rgb;
	gl_FragColor = vec4(1.0 / pow(vec3(2.0), 5.0 * c), 1.0);
}
