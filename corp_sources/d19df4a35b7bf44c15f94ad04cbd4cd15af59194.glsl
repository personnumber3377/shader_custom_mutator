precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	vec2 c = 2.0 * (color.rg - 0.5);
	if(c[0] > 0.0) c[0] = 1.0 * c[0];
	if(c[0] < 0.0) c[0] = -1.0 * c[0];
	if(c[1] > 0.0) c[1] = 1.0 * c[1];
	if(c[1] < 0.0) c[1] = -1.0 * c[1];
	gl_FragColor = vec4(c, 0.0, 1.0);
}
