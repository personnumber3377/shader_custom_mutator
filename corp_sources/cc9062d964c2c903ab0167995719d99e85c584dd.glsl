precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
float gray = 0.0;
void function();
void main ()
{
	gray = 0.0;
	function();
	gl_FragColor = vec4(gray, gray, gray, 1.0);
}
void function()
{
	gray = 1.0;
}
