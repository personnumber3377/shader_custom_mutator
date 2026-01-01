precision mediump float;
precision mediump int;

precision mediump float;
uniform bvec4 color;
void main ()
{
	gl_FragColor = vec4 (float(color[1]), float(color[2]), float(color[3]), 1.0);
}
