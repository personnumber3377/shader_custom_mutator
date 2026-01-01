precision mediump float;
precision mediump int;

vec4 gtf_Color;

vec4 gtf_Vertex = vec4(2.0, 0.5, ((true ? false : (false ? true : true)) ? -1.0 : 2.0), ((true && true) ? 0.5 : -1.0));

uniform mat4 gtf_ModelViewProjectionMatrix;

varying vec4 color;

void main()
{
  const float M_PI = 3.141592653589793;
  vec3 c = ((2.0 * M_PI) * gtf_Color.rgb);
  float sign = -1.0;
  vec3 cos_c = vec3(1.0, 1.0, 1.0);
  float fact = 1.0;
  for (int i = 2; (i <= 20); (i += 2))
  {
    (fact *= (float(i) * float((i - 1))));
    (cos_c += ((sign * pow(c, vec3(float(i), float(i), float(i)))) / fact));
    sign = -sign;
  }
  color = vec4(((0.5 * cos_c) + 0.5), 1.0);
  gl_Position = (gtf_ModelViewProjectionMatrix * gtf_Vertex);
}

