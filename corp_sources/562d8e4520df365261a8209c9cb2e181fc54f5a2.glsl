precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	vec4 al = color;
	vec3 m = al.xyz;
	vec3 t = m.zyx;
	vec4 a = vec4(t.z, t.y, t.x ,al.w);
	gl_FragColor = a;
}
