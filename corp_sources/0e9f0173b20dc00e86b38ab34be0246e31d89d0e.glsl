precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	float c = 2.0 * (color.r - 0.5);
	if(c > 0.0) c = 1.0 * c;
	if(c < 0.0) c = -1.0 * c;
	gl_FragColor = vec4(c, 0.0, 0.0, 1.0);
}
