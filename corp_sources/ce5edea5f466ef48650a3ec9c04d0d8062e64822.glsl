precision mediump float;
precision mediump int;

precision mediump float;
uniform bool color;
void main ()
{
	gl_FragColor = vec4 (float(color), 0.0, 0.0, 1.0);
}
