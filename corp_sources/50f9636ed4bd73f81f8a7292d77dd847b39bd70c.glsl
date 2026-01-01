precision mediump float;
precision mediump int;

attribute vec4 gtf_Vertex;
uniform mat4 gtf_ModelViewProjectionMatrix;
varying vec4 color;
void main ()
{
	int m = 102;
	int k = 12;
	int resultadd = m + k;
	int resultsubtract = m - k;
	float gray;
	if( ( resultadd == 114 ) && ( resultsubtract == 90 ) )
	gray=1.0;
	else gray=0.0;
	color = vec4(gray, gray, gray, 1.0);
	gl_Position = gtf_ModelViewProjectionMatrix * gtf_Vertex;
}
