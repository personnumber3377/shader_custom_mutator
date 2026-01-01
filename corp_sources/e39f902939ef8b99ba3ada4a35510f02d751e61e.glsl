precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void initialise_array(out float array[2], float init_val);
void main ()
{
	int i=0;
	float new_mad[2];
	float gray = 0.0;
	initialise_array(new_mad,25.0);
	if( (new_mad[0] == 25.0) && (new_mad[1] == 25.0) )
	  gray=1.0;
	else gray=0.0;
	gl_FragColor = vec4(gray, gray, gray, 1.0);
}
void initialise_array(out float array[2], float init_val)
{
	int i=0;
	array[0] = init_val;
	array[1] = init_val;
}
