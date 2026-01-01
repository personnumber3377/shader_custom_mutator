precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	mat2 m = mat2(color.r, color.g, color.b, color.a);
	vec4 black = vec4(0.0, 0.0, 0.0, 1.0);
	vec4 result = vec4(1.0, 1.0, 1.0, 1.0);
	if(m[0][0] != color.r) result = black;
	if(m[0][1] != color.g) result = black;
	if(m[1][0] != color.b) result = black;
	if(m[1][1] != color.a) result = black;
	gl_FragColor = result;
}
