precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	vec2 c = floor(10.0 * color.rg - 4.5);
	vec2 result = vec2(equal(ivec2(c), ivec2(0)));
	gl_FragColor = vec4(result, 0.0, 1.0);
}
