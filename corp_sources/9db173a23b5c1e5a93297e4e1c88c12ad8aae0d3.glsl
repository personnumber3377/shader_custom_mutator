precision mediump float;
precision mediump int;

precision mediump float;
varying vec2 col;
void main ()
{
	gl_FragColor = vec4 (col[0], col[1], 0.0, 1.0);
}
