precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	const float edge0 = 0.25;
	const float edge1 = 0.75;
	gl_FragColor = vec4(smoothstep(edge0, edge1, color.r), 0.0, 0.0, 1.0);
}
