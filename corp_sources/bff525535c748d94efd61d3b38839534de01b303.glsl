precision mediump float;
precision mediump int;

precision mediump float;
struct sabcd
{
	float a;
	float b;
	float c;
	float d;
};
void main ()
{
	sabcd s = sabcd(1.0, 2.0, 4.0, 8.0);
	gl_FragColor = vec4(vec3((s.a + s.b + s.c + s.d) / 15.0), 1.0);
}
