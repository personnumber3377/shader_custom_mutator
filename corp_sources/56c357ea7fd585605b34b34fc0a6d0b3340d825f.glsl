precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	vec3 c = 31.0 * color.rgb + 1.0;
	gl_FragColor = vec4(log2(c) / 5.0, 1.0);
}
