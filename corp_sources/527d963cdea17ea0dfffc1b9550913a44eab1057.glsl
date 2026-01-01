precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	const vec2 edge0 = vec2(0.25, 0.25);
	const vec2 edge1 = vec2(0.75, 0.75);
	gl_FragColor = vec4(smoothstep(edge0, edge1, color.rg), 0.0, 1.0);
}
