precision mediump float;
precision mediump int;

precision mediump float;
void main ()
{
	float x;
	mat3 a = mat3( 1.0, 2.0, 3.0,
	               4.0, 5.0, 6.0,
	               7.0, 8.0, 9.0);
	bool elms = true;
	if(a[0][0] != 1.0) elms = false;
	if(a[0][1] != 2.0) elms = false;
	if(a[0][2] != 3.0) elms = false;
	if(a[1][0] != 4.0) elms = false;
	if(a[1][1] != 5.0) elms = false;
	if(a[1][2] != 6.0) elms = false;
	if(a[2][0] != 7.0) elms = false;
	if(a[2][1] != 8.0) elms = false;
	if(a[2][2] != 9.0) elms = false;
	bool rows = true;
	x = a[0][0] + a[1][0] + a[2][0];
	if( x < 12.0-0.1 || x > 12.0+0.1 ) rows = false;
	x = a[0][1] + a[1][1] + a[2][1];
	if(x < 15.0-0.1 || x > 15.0+0.1 ) rows = false;
	x = a[0][2] + a[1][2] + a[2][2];
	if(x < 18.0-0.1 || x > 18.0+0.1 ) rows = false;
	bool cols = true;
	x = a[0][0] + a[0][1] + a[0][2];
	if( x < 6.0-0.1 || x > 6.0+0.1 ) cols = false;
	x = a[1][0] + a[1][1] + a[1][2];
	if(x < 15.0-0.1 || x > 15.0+0.1) cols = false;
	x = a[2][0] + a[2][1] + a[2][2];
	if(x < 24.0-0.1 || x > 24.0+0.1) cols = false;
	float gray = elms && rows && cols ? 1.0 : 0.0;
	gl_FragColor = vec4(gray, gray, gray, 1.0);
}
