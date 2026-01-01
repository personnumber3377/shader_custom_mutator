precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	gl_FragColor = vec4(vec3(distance(color.rgb, vec3(0.5))), 1.0);
}
