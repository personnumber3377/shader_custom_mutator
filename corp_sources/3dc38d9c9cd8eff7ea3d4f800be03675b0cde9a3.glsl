precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	int m = 102;
	int k = 12;
	bool lessthan  = (m<k);
	bool greaterthan = (m>k);
	bool lessthanorequalto = (m <= 102);
	bool greaterthanorequalto = (k >=12);
	float gray;
	if( !lessthan && greaterthan && lessthanorequalto && greaterthanorequalto )
	gray=1.0;
	else gray=0.0;
	gl_FragColor = vec4(gray, gray, gray, 1.0);
}
