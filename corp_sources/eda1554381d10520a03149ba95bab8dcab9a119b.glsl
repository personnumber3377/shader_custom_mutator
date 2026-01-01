precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	gl_FragColor = vec4(vec3(dot(color.rgb, vec3(0.3333))), 1.0);
}
