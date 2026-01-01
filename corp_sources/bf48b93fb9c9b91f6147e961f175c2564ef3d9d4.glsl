precision mediump float;
precision mediump int;

precision mediump float;
struct sabcd
{
	bvec2 a;
	bvec3 b;
	bvec4 c;
};
void main ()
{
	sabcd s = sabcd( bvec2(12, 13), bvec3(14.0, 0.0, 139.0), bvec4(25.5, 17.0, 145, 163 ) );
	float gray = 0.0;
	if( (s.a[0]) && (s.a[1]) && (s.b[0]) && (!s.b[1]) && (s.b[2]) && (s.c[0]) && (s.c[1]) && (s.c[2]) )
	  gray=1.0;
	else
          gray =0.0;
	gl_FragColor = vec4(gray, gray, gray, 1.0);
}
