precision mediump float;
precision mediump int;

precision mediump float;
precision mediump float;
varying vec4 color;
void main ()
{
	vec2 c = floor(1.5 * color.rg);
	gl_FragColor = vec4(vec2(not(bvec2(c))), 0.0, 1.0);
}
