precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	const float M_PI = 3.14159265358979323846;
	vec3 v1;
	vec3 v2 = normalize(vec3(1.0, 1.0, 1.0));
	float theta = color.g * 2.0 * M_PI;
	float phi = color.b * 2.0 * M_PI;
	v1.x = cos(theta) * sin(phi);
	v1.y = sin(theta) * sin(phi);
	v1.z = cos(phi);
	gl_FragColor = vec4((reflect(v1, v2) + 1.0) / 2.0, 1.0);
}
