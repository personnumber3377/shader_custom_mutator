precision mediump float;
precision mediump int;

attribute vec4 gtf_Vertex;
uniform mat4 gtf_ModelViewProjectionMatrix;
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
	color = vec4(gray, gray, gray, 1.0);
	gl_Position = gtf_ModelViewProjectionMatrix * gtf_Vertex;
}
