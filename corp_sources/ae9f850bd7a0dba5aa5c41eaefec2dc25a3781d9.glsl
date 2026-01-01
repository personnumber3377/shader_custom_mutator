precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	const vec3 min_c = vec3(0.25, 0.25, 0.25);
	const vec3 max_c = vec3(0.75, 0.75, 0.75);
	vec3 c = color.rgb;
	if(c[0] < min_c[0]) c[0] = min_c[0];
	if(c[1] < min_c[1]) c[1] = min_c[1];
	if(c[2] < min_c[2]) c[2] = min_c[2];
	if(c[0] > max_c[0]) c[0] = max_c[0];
	if(c[1] > max_c[1]) c[1] = max_c[1];
	if(c[2] > max_c[2]) c[2] = max_c[2];
	gl_FragColor = vec4(c, 1.0);
}
