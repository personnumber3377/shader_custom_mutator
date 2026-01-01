precision mediump float;
precision mediump int;

precision mediump float;
precision mediump float;
varying vec4 color;
void main ()
{
	vec2 c = floor(1.5 * color.rg);
	vec2 result = vec2(equal(bvec2(c), bvec2(true)));
	gl_FragColor = vec4(result, 0.0, 1.0);
}
