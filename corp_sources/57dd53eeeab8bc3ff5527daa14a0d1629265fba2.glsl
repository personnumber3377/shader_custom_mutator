precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	int m = +23;
	int k = -m;
	bool a = false;
	bool b = !a;
	float gray;
	if( (m==23) && (k==-23) && (b) )
	gray=1.0;
	else gray=0.0;
	gl_FragColor = vec4(gray, gray, gray, 1.0);
}
