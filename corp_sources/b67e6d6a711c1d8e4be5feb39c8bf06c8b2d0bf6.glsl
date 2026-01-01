precision mediump float;
precision mediump int;

precision mediump float;
uniform float funi1;
uniform vec2 funi2;
uniform vec3 funi3;
uniform vec4 funi4;
varying vec4 color;
void main ()
{
	vec4 temp = vec4(funi1, funi2[0] + funi2[1], funi3[0] + funi3[1] + funi3[2], funi4[0] + funi4[1] + funi4[2] + funi4[3]);
	gl_FragColor = temp + color;
}
