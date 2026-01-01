precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	gl_FragColor = vec4(vec3(sqrt(color.r*color.r + color.g*color.g + color.b*color.b) / 3.0), 1.0);
}
