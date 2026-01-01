precision mediump float;
precision mediump int;

attribute vec4 gtf_Color;
attribute vec4 gtf_Vertex;
uniform mat4 gtf_ModelViewProjectionMatrix;
varying vec4 color;
void main ()
{
	vec3 x = (gtf_Color.rgb + 0.01) / 1.01;
	vec3 y = vec3(0.0);
	vec3 z;
	int n = 50;
	z = abs((x - 1.0) / (x + 1.0));
	vec3 p = z;
	for(int i = 1; i <= 101; i += 2)
	{
		y += p / float(i);
		p *= z * z;
	}
	y *= -2.0;
	color = vec4(y / -4.61, 1.0);
	gl_Position = gtf_ModelViewProjectionMatrix * gtf_Vertex;
}
