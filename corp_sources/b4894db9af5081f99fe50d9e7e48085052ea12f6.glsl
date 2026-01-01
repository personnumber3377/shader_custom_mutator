precision mediump float;
precision mediump int;

vec4 gtf_Vertex;

vec4 gtf_Color;

uniform mat4 gtf_ModelViewProjectionMatrix;

varying vec4 color;

void main()
{
  const float M_PI = 3.141592653589793;
  vec3 c = (2.0 * (gtf_Color.rgb - 0.5));
  vec3 acos_c = vec3(0.0);
  vec3 scale = vec3(1.0);
  vec3 sign = vec3(1.0);
  if ((c.r < 0.0))
  {
    sign.r = -1.0;
    (c.r *= -1.0);
  }
  for (int i = 1; (i < 1000); (i += 2))
  {
    (acos_c.r += ((scale.r * pow(c.r, float(i))) / float(i)));
    (scale.r *= (float(i) / float((i + 1))));
  }
  acos_c.r = ((M_PI / 2.0) - (sign.r * acos_c.r));
  if ((c.g < 0.0))
  {
    sign.g = -1.0;
    (c.g *= -1.0);
  }
  for (int i = 1; (i < 1000); (i += 2))
  {
    (acos_c.g += ((scale.g * pow(c.g, float(i))) / float(i)));
    (scale.g *= (float(i) / float((i + 1))));
  }
  acos_c.g = ((M_PI / 2.0) - (sign.g * acos_c.g));
  if ((c.b < 0.0))
  {
    sign.b = -1.0;
    (c.b *= -1.0);
  }
  for (int i = 1; (i < 1000); (i += 2))
  {
    (acos_c.b += ((scale.b * pow(c.b, float(i))) / float(i)));
    (scale.b *= (float(i) / float((i + 1))));
  }
  acos_c.b = ((M_PI / 2.0) - (sign.b * acos_c.b));
  color = vec4((acos_c / M_PI), 1.0);
  gl_Position = (gtf_ModelViewProjectionMatrix * gtf_Vertex);
}

