precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	ivec3 a = ivec3(20, 13, 17);
	float gray;
	if( (a[0] == 20) && (a[1] == 13) && (a[2] == 17) )
	gray=1.0;
	else gray=0.0;
	gl_FragColor = vec4(gray, gray, gray, 1.0);
}
