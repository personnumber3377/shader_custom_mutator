precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	vec3 c = (color.rgb * 99.0) + 1.0;
	gl_FragColor = vec4(1.0 / sqrt(c), 1.0);
}
