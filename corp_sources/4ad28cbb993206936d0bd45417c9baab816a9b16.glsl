precision mediump float;
precision mediump int;

precision mediump float;
uniform ivec2 color;
void main ()
{
	gl_FragColor = vec4 (color[0], color[1], 0.0, 1.0);
}
