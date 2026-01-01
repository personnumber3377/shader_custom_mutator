precision mediump float;
precision mediump int;

precision mediump float;
uniform bool funi1;
uniform bvec2 funi2;
uniform bvec3 funi3;
uniform bvec4 funi4;
varying vec4 color;
void main ()
{
	vec4 temp = vec4(0.0, 0.0, 0.0, 0.0);
	if(funi1 || funi2[0] && funi2[1] && funi3[0] && funi3[1] && funi3[2] || funi4[0] && funi4[1] && funi4[2] && funi4[3])
		temp = vec4(1.0, 0.0, 0.5, 1.0);
	gl_FragColor = temp + color;
}
