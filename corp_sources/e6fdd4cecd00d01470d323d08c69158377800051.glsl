precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	mat3 m1 = mat3(color.rgb, color.rgb, color.rgb);
	mat3 m2 = mat3(1.0, 0.5, 0.5, 0.5, 1.0, 0.5, 0.5, 0.5, 1.0);
	mat3 m3 = mat3(0.0);
	vec3 result = vec3(0.0, 0.0, 0.0);
	m3 = matrixCompMult(m1, m2);
	result[0] += m3[0][0];
	result[0] += m3[0][1];
	result[0] += m3[0][2];
	result[1] += m3[1][0];
	result[1] += m3[1][1];
	result[1] += m3[1][2];
	result[2] += m3[2][0];
	result[2] += m3[2][1];
	result[2] += m3[2][2];
	gl_FragColor = vec4(result / 2.0, 1.0);
}
