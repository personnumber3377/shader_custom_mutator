precision mediump float;
precision mediump int;

precision mediump float;
uniform bvec3 color;
void main ()
{
	gl_FragColor = vec4 (vec3(color), 1.0);
}
