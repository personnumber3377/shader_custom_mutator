precision mediump float;
precision mediump int;

precision mediump float;
uniform ivec4 color;
void main ()
{
	gl_FragColor = vec4 (color[0], color[1], color[2], color[3]);
}
