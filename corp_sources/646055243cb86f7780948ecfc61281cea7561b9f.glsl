precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	int m = 102;
	int k = 12;
	int result = m*k;
	float gray;
	if( ( result == 1224 ) )
	gray=1.0;
	else gray=0.0;
	gl_FragColor = vec4(gray, gray, gray, 1.0);
}
