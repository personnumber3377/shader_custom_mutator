precision mediump float;
precision mediump int;

precision mediump float;
void main ()
{
	float x;
	mat2 a = mat2(1.0, 2.0,
	              4.0, 8.0);
	bool elms = true;
	if(a[0][0] != 1.0) elms = false;
	if(a[0][1] != 2.0) elms = false;
	if(a[1][0] != 4.0) elms = false;
	if(a[1][1] != 8.0) elms = false;
	bool rows = true;
	x = a[0][0] + a[1][0];
	if(x < 5.0-0.1 || x > 5.0+0.1) rows = false;
	x = a[0][1] + a[1][1];
	if(x < 10.0-0.1 || x > 10.0+0.1) rows = false;
	bool cols = true;
	x = a[0][0] + a[0][1];
	if(x < 3.0-0.1 || x > 3.0+0.1) cols = false;
	x = a[1][0] + a[1][1];
	if(x < 12.0-0.1 || x > 12.0+0.1) cols = false;
	float gray = elms && rows && cols ? 1.0 : 0.0;
	gl_FragColor = vec4(gray, gray, gray, 1.0);
}
