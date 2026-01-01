precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	vec3 b = vec3(13.0, 53.0, 139.0);
	vec2 a = vec2(b);
	float gray;
	if( (a[0] == 13.0) && (a[1] == 53.0) )
	gray=1.0;
	else gray=0.0;
	gl_FragColor = vec4(gray, gray, gray, 1.0);
}
