precision mediump float;
precision mediump int;

attribute vec4 gtf_Vertex;
uniform mat4 gtf_ModelViewProjectionMatrix;
varying vec4 color;
struct sabcd
{
	bool a;
	bool b;
	bool c;
	bool d;
};
void main ()
{
	sabcd s = sabcd(bool(12), bool(0), bool(25.5), bool(0.0));
	float gray = 0.0;
	if( (s.a==true) && (s.b==false) && (s.c == true) && (s.d==false))
	  gray=1.0;
	else
          gray =0.0;
	color = vec4(gray, gray, gray, 1.0);
	gl_Position = gtf_ModelViewProjectionMatrix * gtf_Vertex;
}
