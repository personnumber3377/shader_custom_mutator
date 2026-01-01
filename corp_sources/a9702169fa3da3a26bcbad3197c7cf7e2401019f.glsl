precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 col;
void main ()
{
	gl_FragColor = vec4 (col[1], col[2], col[3], 1.0);
}
