precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	vec3 c = floor(1.5 * color.rgb);
	gl_FragColor = vec4(vec3(any(bvec3(c))), 1.0);
}
