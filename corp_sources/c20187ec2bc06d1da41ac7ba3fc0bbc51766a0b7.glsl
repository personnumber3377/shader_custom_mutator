precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	const float edge = 0.5;
	float c = color.r;
	if(c >= edge) c = 1.0;
	else c = 0.0;
	gl_FragColor = vec4(c, 0.0, 0.0, 1.0);
}
