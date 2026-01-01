precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	const vec3 edge0 = vec3(0.25, 0.25, 0.25);
	const vec3 edge1 = vec3(0.75, 0.75, 0.75);
	gl_FragColor = vec4(smoothstep(edge0, edge1, color.rgb), 1.0);
}
