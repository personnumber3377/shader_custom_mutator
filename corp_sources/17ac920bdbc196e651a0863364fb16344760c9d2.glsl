precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 col;
void main ()
{
	gl_FragColor = vec4 (col[0], col[1], col[2], 1.0);
}
