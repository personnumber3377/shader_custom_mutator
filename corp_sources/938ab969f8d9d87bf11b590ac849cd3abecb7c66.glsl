precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
struct sabcd
{
 mat2 a;
};
void main ()
{
	sabcd s = sabcd(mat2(12.0, 29.0, 13.0, 26.0) );
	gl_FragColor =  vec4( vec3(  (s.a[0][0] + s.a[0][1] + s.a[1][0] + s.a[1][1]) / 80.0  ), 1.0);
}
