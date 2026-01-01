precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	vec3 c = floor(1.5 * color.rgb);
	vec3 result = vec3(equal(bvec3(c), bvec3(true)));
	gl_FragColor = vec4(result, 1.0);
}
