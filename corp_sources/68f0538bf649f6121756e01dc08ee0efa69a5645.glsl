precision mediump float;
precision mediump int;

precision mediump float;
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
	gl_FragColor = vec4(gray, gray, gray, 1.0);
}
