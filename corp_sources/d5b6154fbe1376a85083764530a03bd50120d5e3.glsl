precision mediump float;
precision mediump int;

precision mediump float;
struct sabcd
{
	vec2 a;
	vec2 b;
};
void main ()
{
	sabcd s = sabcd(vec2(12.0, 29.0), vec2(13.0, 26.0) );
	gl_FragColor =  vec4( vec3(  (s.a[0] + s.a[1] + s.b[0] + s.b[1]) / 80.0  ), 1.0);
}
