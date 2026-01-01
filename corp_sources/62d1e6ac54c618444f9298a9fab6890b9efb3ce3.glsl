precision mediump float;
precision mediump int;

attribute vec4 gtf_Color;
attribute vec4 gtf_Vertex;
uniform mat4 gtf_ModelViewProjectionMatrix;
varying vec4 color;
const float ln2 = 0.69314718055994530941723212145818;
void main ()
{
	float x = (gtf_Color.r + 0.01) / 1.01;
	float y = 0.0;
	float z;
	int n = 50;
	z = abs((x - 1.0) / (x + 1.0));
	float p = z;
	for(int i = 1; i <= 101; i += 2)
	{
		y += p / float(i);
		p *= z * z;
	}
	y *= -2.0 / ln2;
	color = vec4(y / -8.0, 0.0, 0.0, 1.0);
	gl_Position = gtf_ModelViewProjectionMatrix * gtf_Vertex;
}
