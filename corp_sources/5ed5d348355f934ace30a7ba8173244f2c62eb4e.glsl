precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	vec2 c = floor(4.0 * color.rg);
	gl_FragColor = vec4(vec3(all(bvec2(c))), 1.0);
}
