precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	const float M_PI = 3.14159265358979323846;
	vec2 c = 2.0 * M_PI * ( fract(abs(color.rg)) - 0.5 );
	float sign =  1.0;
	vec2 cos_c = vec2(-1.0, -1.0);
	float fact_even = 1.0;
	float fact_odd  = 1.0;
	vec2 sum;
	vec2 exp;
	for(int i = 2; i <= 10; i += 2)
	{
		fact_even *= float(i);
		fact_odd  *= float(i-1);
		exp = vec2(float(i/2), float(i/2));
		sum = sign * pow(abs(c), exp)/fact_even;
		cos_c += pow(abs(c), exp)*(sum/fact_odd);
		sign = -sign;
	}
	gl_FragColor = vec4(0.5 * cos_c + 0.5, 0.0, 1.0);
}
