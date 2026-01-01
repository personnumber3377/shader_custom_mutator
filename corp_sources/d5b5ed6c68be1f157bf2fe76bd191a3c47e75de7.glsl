precision mediump float;
precision mediump int;

precision mediump float;
uniform ivec4 color[2];
void main ()
{
	float r = float(color[0][0] + color[0][1] + color[0][2] + color[0][3]);
	float g = float(color[1][0] + color[1][1] + color[1][2] + color[1][3]);
	gl_FragColor = vec4 (r/256.0, g/256.0, 0.0, 1.0);
}
