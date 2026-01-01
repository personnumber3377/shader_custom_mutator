precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	vec3 c = 31.0 * color.rgb + 1.0;
	gl_FragColor = vec4(log(c) / 3.466, 1.0);
}
