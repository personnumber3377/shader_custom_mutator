precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	int m = 102;
	int k = 12;
	bool equalto = (m == 102);
	bool notequalto = (k != 102);
	float gray;
	if( equalto && notequalto )
	gray=1.0;
	else gray=0.0;
	gl_FragColor = vec4(gray, gray, gray, 1.0);
}
