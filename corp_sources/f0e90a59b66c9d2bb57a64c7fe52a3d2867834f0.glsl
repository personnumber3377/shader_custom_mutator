precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	if(color.r > 0.75 || color.g > 0.75 || color.b > 0.75)
	{
		gl_FragColor = vec4(0.0, 0.0, 0.0, 0.0);
	}
	else
	{
		gl_FragColor = color;
	}
}
