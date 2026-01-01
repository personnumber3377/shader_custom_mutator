precision mediump float;
precision mediump int;

precision mediump float;
uniform bvec2 color;
void main ()
{
	gl_FragColor = vec4 (vec2(color), 0.0, 1.0);
}
