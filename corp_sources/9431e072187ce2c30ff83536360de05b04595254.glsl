precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	int i=0;
	float new_mad[2];
	float gray = 0.0;
	new_mad[0]=float(1);
	new_mad[1]=float(2);
	if( (new_mad[0] == 1.0) && (new_mad[1] == 2.0) )
	  gray=1.0;
	else gray=0.0;
	gl_FragColor = vec4(gray,gray , gray, 1.0);
}
