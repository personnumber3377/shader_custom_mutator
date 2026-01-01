precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	mat4 a = mat4( 1.0, 2.0, 3.0, 4.0,
				   5.0, 6.0, 7.0, 8.0,
                   9.0, 10.0, 11.0, 12.0,
                  13.0, 14.0, 15.0, 16.0);
	float gray,sum1=0.0,sum2=0.0,sum3=0.0,sum4=0.0;
	int i;
	sum1 += a[0][0];
	sum2 += a[1][0];
	sum3 += a[2][0];
	sum4 += a[3][0];
	sum1 += a[0][1];
	sum2 += a[1][1];
	sum3 += a[2][1];
	sum4 += a[3][1];
	sum1 += a[0][2];
	sum2 += a[1][2];
	sum3 += a[2][2];
	sum4 += a[3][2];
	sum1 += a[0][3];
	sum2 += a[1][3];
	sum3 += a[2][3];
	sum4 += a[3][3];
	if( ( sum1 > 10.0-0.1 && sum1 < 10.0+0.1  ) &&
		( sum2 > 26.0-0.1 && sum2 < 26.0+0.1) &&
		( sum3 > 42.0-0.1 && sum3 < 42.0+0.1) &&
		( sum4 > 58.0-0.1 && sum4 < 58.0+0.1) )
	gray=1.0;
	else gray=0.0;
	gl_FragColor = vec4(gray, gray, gray, 1.0);
}
