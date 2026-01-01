precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	gl_FragColor = vec4(vec3(sqrt(pow(abs(color.r - 0.5), 2.0) + pow(abs(color.g - 0.5), 2.0) + pow(abs(color.b - 0.5), 2.0))), 1.0);
}
