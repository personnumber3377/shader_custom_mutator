precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	gl_FragColor = vec4(vec3(dot(color.r, 1.0)), 1.0);
}
