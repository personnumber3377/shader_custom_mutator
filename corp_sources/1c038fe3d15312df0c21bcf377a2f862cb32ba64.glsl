precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	bvec4 a = bvec4(0, 23, 0.0, 23.0);
	float gray;
	if( (a[0] == false) && (a[1] == true) && (a[2] == false) && (a[3] == true) )
	gray=1.0;
	else gray=0.0;
	gl_FragColor = vec4(gray, gray, gray, 1.0);
}
