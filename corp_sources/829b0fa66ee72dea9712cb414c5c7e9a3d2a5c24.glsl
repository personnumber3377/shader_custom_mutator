precision mediump float;
precision mediump int;

precision mediump float;
void main ()
{
	float x;
	const mat2 a = mat2(1.0, 2.0,
	                    4.0, 8.0);
	mat2 b = a;
	bool elms = true;
	if(b[0][0] != 1.0) elms = false;
	if(b[0][1] != 2.0) elms = false;
	if(b[1][0] != 4.0) elms = false;
	if(b[1][1] != 8.0) elms = false;
	bool rows = true;
	x = b[0][0] + b[1][0];
	if(x < 5.0-0.1 || x > 5.0+0.1) rows = false;
	x = b[0][1] + b[1][1];
	if(x < 10.0-0.1 || x > 10.0+0.1) rows = false;
	bool cols = true;
	x = b[0][0] + b[0][1];
	if(x < 3.0-0.1 || x > 3.0+0.1) cols = false;
	x = b[1][0] + b[1][1];
	if(x < 12.0-0.1 || x > 12.0+0.1) cols = false;
	float gray = elms && rows && cols ? 1.0 : 0.0;
	gl_FragColor = vec4(gray, gray, gray, 1.0);
}
