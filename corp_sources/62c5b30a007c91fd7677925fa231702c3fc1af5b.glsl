precision mediump float;
precision mediump int;

attribute vec4 gtf_Vertex;
uniform mat4 gtf_ModelViewProjectionMatrix;
varying vec4 color;
void main ()
{
	float x;
	mat4 a = mat4(   1.0,    2.0,     4.0,     8.0,
	                16.0,   32.0,    64.0,   128.0,
	               256.0,  512.0,  1024.0,  2048.0,
	              4096.0, 8192.0, 16384.0, 32768.0);
	bool elms = true;
	if(a[0][0] !=     1.0) elms = false;
	if(a[0][1] !=     2.0) elms = false;
	if(a[0][2] !=     4.0) elms = false;
	if(a[0][3] !=     8.0) elms = false;
	if(a[1][0] !=    16.0) elms = false;
	if(a[1][1] !=    32.0) elms = false;
	if(a[1][2] !=    64.0) elms = false;
	if(a[1][3] !=   128.0) elms = false;
	if(a[2][0] !=   256.0) elms = false;
	if(a[2][1] !=   512.0) elms = false;
	if(a[2][2] !=  1024.0) elms = false;
	if(a[2][3] !=  2048.0) elms = false;
	if(a[3][0] !=  4096.0) elms = false;
	if(a[3][1] !=  8192.0) elms = false;
	if(a[3][2] != 16384.0) elms = false;
	if(a[3][3] != 32768.0) elms = false;
	bool rows = true;
	x = a[0][0] + a[1][0] + a[2][0] + a[3][0];
	if(x < 4369.0-0.1 || x > 4369.0+0.1) rows = false;
	x = a[0][1] + a[1][1] + a[2][1] + a[3][1];
	if(x < 8738.0-0.1 || x > 8738.0+0.1) rows = false;
	x = a[0][2] + a[1][2] + a[2][2] + a[3][2];
	if(x < 17476.0-0.1 || x > 17476.0+0.1) rows = false;
	x = a[0][3] + a[1][3] + a[2][3] + a[3][3];
	if(x < 34952.0-0.1 || x > 34952.0+0.1) rows = false;
	bool cols = true;
	x = a[0][0] + a[0][1] + a[0][2] + a[0][3];
	if(x < 15.0-0.1 || x > 15.0+0.1) cols = false;
	x = a[1][0] + a[1][1] + a[1][2] + a[1][3];
	if(x < 240.0-0.1 || x > 240.0+0.1) cols = false;
	x = a[2][0] + a[2][1] + a[2][2] + a[2][3];
	if(x < 3840.0-0.1 || x > 3840.0+0.1) cols = false;
	x = a[3][0] + a[3][1] + a[3][2] + a[3][3];
	if(x < 61440.0-0.1 || x > 61440.0+0.1) cols = false;
	float gray = elms && rows && cols ? 1.0 : 0.0;
	color = vec4(gray, gray, gray, 1.0);
	gl_Position = gtf_ModelViewProjectionMatrix * gtf_Vertex;
}
