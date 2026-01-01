precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	vec4 al = color;
	float x = al.x;
	float y = al.y;
	float z = al.z;
	float w = al.w;
	vec4 m = vec4(x,y,z,w);
	gl_FragColor = m;
}
