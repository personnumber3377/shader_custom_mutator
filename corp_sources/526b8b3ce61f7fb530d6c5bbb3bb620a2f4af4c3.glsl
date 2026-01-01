precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	mat2 m1 = mat2(color.rg, color.ba);
	mat2 m2 = mat2(1.0, 0.5, 0.5, 1.0);
	mat2 m3 = mat2(0.0);
	m3[0][0] = m1[0][0] * m2[0][0];
	m3[0][1] = m1[0][1] * m2[0][1];
	m3[1][0] = m1[1][0] * m2[1][0];
	m3[1][1] = m1[1][1] * m2[1][1];
	gl_FragColor = vec4(m3[0][0], m3[1][0], m3[0][1], m3[1][1]);
}
