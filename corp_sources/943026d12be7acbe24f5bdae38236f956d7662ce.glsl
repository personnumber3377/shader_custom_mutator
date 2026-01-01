precision mediump float;
precision mediump int;

precision mediump float;
uniform ivec2 color[2];
void main ()
{
	float r = float(color[0][0]);
	float g = float(color[0][1]);
	float b = float(color[1][0]);
	float a = float(color[1][1]);
	gl_FragColor = vec4 (r/256.0, g/256.0, b/256.0, a/256.0);
}
