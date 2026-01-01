precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	gl_FragColor = vec4(vec3(color.r + color.g + color.b) * 0.3333, 1.0);
}
