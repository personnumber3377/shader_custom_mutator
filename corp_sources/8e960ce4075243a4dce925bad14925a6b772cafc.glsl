precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	int m = 102;
	int k = 12;
	int resultadd = m + k;
	int resultsubtract = m - k;
	float gray;
	if( ( resultadd == 114 ) && ( resultsubtract == 90 ) )
	gray=1.0;
	else gray=0.0;
	gl_FragColor = vec4(gray, gray, gray, 1.0);
}
