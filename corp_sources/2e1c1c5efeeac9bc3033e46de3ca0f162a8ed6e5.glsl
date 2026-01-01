precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
struct sabcd
{
	vec4 a;
	vec4 b;
};
void main ()
{
	sabcd s = sabcd(vec4(12.0, 29.0, 32.0, 47.0), vec4(13.0, 26.0, 38.0, 53.0 ) );
	gl_FragColor = vec4( vec3(  (s.a[0] + s.a[1] + s.a[2] + s.a[3] + s.b[0] + s.b[1] + s.b[2] + s.b[3]) / 250.0  ), 1.0);
}
