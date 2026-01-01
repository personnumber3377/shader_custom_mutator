precision mediump float;
precision mediump int;

vec4 gtf_Color = vec4(1.0, (!true ? ((true || false) ? +1.0 : -1.0) : (!true ? (-1.0 / 0.0) : 0.5)), -2.0, 0.0);

vec4 gtf_Vertex = vec4(-0.5, -0.5, 0.0, 1.0);

uniform mat4 gtf_ModelViewProjectionMatrix;

varying vec4 color;

void main()
{
  const float M_PI = 3.141592653589793;
  float c = ((2.0 * M_PI) * gtf_Color.r);
  float sign = 1.0;
  float sin_c = 0.0;
  float fact;
  float fact_of;
  for (int i = 0; (i < 12); i++)
  {
    fact = 1.0;
    for (int j = 2; (j <= 23); j++)
    if ((j <= ((2 * i) + 1)))
      (fact *= float(j));
    (sin_c += ((sign * pow(c, ((2.0 * float(i)) + 1.0))) / fact));
    (sign *= -1.0);
  }
  color = vec4(((0.5 * sin_c) + 0.5), 0.0, 0.0, 1.0);
  gl_Position = (gtf_ModelViewProjectionMatrix * gtf_Vertex);
}

