precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	vec3 c = 2.0 * (color.rgb - 0.5);
	if(c[0] > 0.0) c[0] = 1.0 * c[0];
	if(c[0] < 0.0) c[0] = -1.0 * c[0];
	if(c[1] > 0.0) c[1] = 1.0 * c[1];
	if(c[1] < 0.0) c[1] = -1.0 * c[1];
	if(c[2] > 0.0) c[2] = 1.0 * c[2];
	if(c[2] < 0.0) c[2] = -1.0 * c[2];
	gl_FragColor = vec4(c, 1.0);
}
