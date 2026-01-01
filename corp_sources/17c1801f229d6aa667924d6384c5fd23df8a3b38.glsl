precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	vec3 c = floor(10.0 * color.rgb - 4.5);
	vec3 result = vec3(lessThanEqual(c, vec3(0.0)));
	gl_FragColor = vec4(result, 1.0);
}
