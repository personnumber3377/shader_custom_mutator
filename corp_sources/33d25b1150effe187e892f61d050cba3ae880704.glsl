precision mediump float;
precision mediump int;

attribute vec4 gtf_Color;
attribute vec4 gtf_Vertex;
uniform mat4 gtf_ModelViewProjectionMatrix;
varying vec4 color;
void main ()
{
	const float M_PI = 3.14159265358979323846;
	vec2 c = 2.0 * M_PI * gtf_Color.rg;
	float sign = -1.0;
	vec2 cos_c = vec2(1.0, 1.0);
	float fact = 1.0;
	for(int i = 2; i <= 20; i += 2)
	{
		fact *= float(i)*float(i-1);
		cos_c += sign*pow(c, vec2(float(i), float(i)))/fact;
		sign = -sign;
	}
	color = vec4(0.5 * cos_c + 0.5, 0.0, 1.0);
	gl_Position = gtf_ModelViewProjectionMatrix * gtf_Vertex;
}
