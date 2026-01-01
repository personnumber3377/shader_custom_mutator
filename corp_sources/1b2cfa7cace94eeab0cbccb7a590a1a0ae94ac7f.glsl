precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	int m = 12;
	int n = 102;
	bool result = true;
	int r = m;
	if( r==12 )
		result = result && true;
	else
		result = result && false;
	r += m;
	if( r == 24 )
		result = result && true;
	else
		result = result && false;
	r-= m;
	if( r == 12 )
		result = result && true;
	else
		result = result && false;
	r*= m;
	if ( r == 144 )
		result = result && true;
	else
		result = result && false;
	r/= m;
	if( r >= 11 && r <= 13 )
		result = result && true;
	else
		result = result && false;
	float gray;
	if( result )
	gray=1.0;
	else gray=0.0;
	gl_FragColor = vec4(gray, gray, gray, 1.0);
}
