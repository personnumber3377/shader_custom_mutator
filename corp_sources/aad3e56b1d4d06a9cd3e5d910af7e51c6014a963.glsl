precision mediump float;
precision mediump int;

vec4 gtf_Vertex = vec4(1.0, -1.0, -(-1.0 / 0.0), ((false ? false : (true || false)) ? 2.0 : (2.0 * (-1.0 * 1.0))));

vec4 gtf_Color = vec4(0.5, ((0.0 + 0.0) + ((0.0 + 2.0) - 0.5)), ((true ? 0.0 : (false ? 0.5 : 2.0)) * 0.5), +-1.0);

uniform mat4 gtf_ModelViewProjectionMatrix;

varying vec4 color;

void main()
{
  const float M_PI = 3.141592653589793;
  vec2 c = (2.0 * (gtf_Color.rg - 0.5));
  vec2 acos_c = vec2(0.0);
  vec2 scale = vec2(1.0);
  vec2 sign = vec2(1.0);
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
  color = vec4((acos_c / M_PI), 0.0, 1.0);
  gl_Position = (gtf_ModelViewProjectionMatrix * gtf_Vertex);
}

