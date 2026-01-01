precision mediump float;
precision mediump int;

precision mediump float;
uniform mat4 color;
void main ()
{
	gl_FragColor = vec4 (color[0][0] + color[0][1] + color[0][2] + color[0][3],
						 color[1][0] + color[1][1] + color[1][2] + color[1][3],
						 color[2][0] + color[2][1] + color[2][2] + color[2][3],
						 color[3][0] + color[3][1] + color[3][2] + color[3][3]);
}
