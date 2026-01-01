precision mediump float;
precision mediump int;

attribute vec4 gtf_Vertex;
uniform mat4 gtf_ModelViewProjectionMatrix;
varying vec4 color;
void main ()
{
	float x;
	mat3 a = mat3( 1.0,   2.0,   4.0,
	               8.0,  16.0,  32.0,
	              64.0, 128.0, 256.0);
	bool elms = true;
	if(a[0][0] !=   1.0) elms = false;
	if(a[0][1] !=   2.0) elms = false;
	if(a[0][2] !=   4.0) elms = false;
	if(a[1][0] !=   8.0) elms = false;
	if(a[1][1] !=  16.0) elms = false;
	if(a[1][2] !=  32.0) elms = false;
	if(a[2][0] !=  64.0) elms = false;
	if(a[2][1] != 128.0) elms = false;
	if(a[2][2] != 256.0) elms = false;
	bool rows = true;
	x = a[0][0] + a[1][0] + a[2][0];
	if( x < 73.0-0.1 || x > 73.0+0.1 ) rows = false;
	x = a[0][1] + a[1][1] + a[2][1];
	if(x < 146.0-0.1 || x > 146.0+0.1 ) rows = false;
	x = a[0][2] + a[1][2] + a[2][2];
	if(x < 292.0-0.1 || x > 292.0+0.1 ) rows = false;
	bool cols = true;
	x = a[0][0] + a[0][1] + a[0][2];
	if( x < 7.0-0.1 || x > 7.0+0.1 ) cols = false;
	x = a[1][0] + a[1][1] + a[1][2];
	if(x < 56.0-0.1 || x > 56.0+0.1) cols = false;
	x = a[2][0] + a[2][1] + a[2][2];
	if(x < 448.0-0.1 || x > 448.0+0.1) cols = false;
	float gray = elms && rows && cols ? 1.0 : 0.0;
	color = vec4(gray, gray, gray, 1.0);
	gl_Position = gtf_ModelViewProjectionMatrix * gtf_Vertex;
}
