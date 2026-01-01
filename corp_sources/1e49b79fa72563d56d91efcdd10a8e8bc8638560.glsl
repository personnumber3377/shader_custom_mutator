precision mediump float;
precision mediump int;

precision mediump float;
uniform int color[2];
void main ()
{
	float r = float(color[0]);
	float g = float(color[1]);
	gl_FragColor = vec4 (r/256.0, g/256.0, 0.0, 1.0);
}
