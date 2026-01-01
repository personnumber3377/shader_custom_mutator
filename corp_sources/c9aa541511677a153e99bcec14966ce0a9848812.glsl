precision mediump float;
precision mediump int;

vec4 gtf_Vertex = vec4(2.0, 0.5, +(!true ? +-1.0 : (true ? 1.0 : -1.0)), 0.0);

vec4 gtf_Color = vec4((false ? ((false ? -1.0 : 2.0) / 2.0) : 0.0), 1.0, +2.0, +(true ? (true ? 1.0 : 0.0) : +-1.0));

uniform mat4 gtf_ModelViewProjectionMatrix;

varying vec4 color;

void main()
{
  const float M_PI = 3.141592653589793;
  vec2 x = (2.0 * (gtf_Color.gg - 0.5));
  vec2 y = (2.0 * (gtf_Color.bb - 0.5));
  vec2 c;
  vec2 atan_c = vec2(0.0);
  vec2 scale = vec2(1.0);
  vec2 sign = vec2(1.0);
  vec4 result = vec4(0.0, 0.0, 0.0, 1.0);
  const float epsilon = 0.0001;
  if (((x[0] > epsilon) || (abs(y[0]) > epsilon)))
  {
    if (((x[0] < 0.0) ^^ (y[0] < 0.0)))
    {
      sign[0] = -1.0;
    }
    if ((abs(y[0]) <= abs(x[0])))
    {
      c[0] = abs((y[0] / x[0]));
      (atan_c[0] += ((scale[0] * pow(c[0], float(1))) / float(1)));
      (scale[0] *= -1.0);
      (atan_c[0] += ((scale[0] * pow(c[0], float(3))) / float(3)));
      (scale[0] *= -1.0);
      (atan_c[0] += ((scale[0] * pow(c[0], float(5))) / float(5)));
      (scale[0] *= -1.0);
      (atan_c[0] += ((scale[0] * pow(c[0], float(7))) / float(7)));
      (scale[0] *= -1.0);
      (atan_c[0] += ((scale[0] * pow(c[0], float(9))) / float(9)));
      (scale[0] *= -1.0);
      (atan_c[0] += ((scale[0] * pow(c[0], float(11))) / float(11)));
      (scale[0] *= -1.0);
      result[0] = (((sign[0] * atan_c[0]) / (2.0 * M_PI)) + 0.5);
    }
    else
    {
      c[0] = abs((x[0] / y[0]));
      (atan_c[0] += ((scale[0] * pow(c[0], float(1))) / float(1)));
      (scale[0] *= -1.0);
      (atan_c[0] += ((scale[0] * pow(c[0], float(3))) / float(3)));
      (scale[0] *= -1.0);
      (atan_c[0] += ((scale[0] * pow(c[0], float(5))) / float(5)));
      (scale[0] *= -1.0);
      (atan_c[0] += ((scale[0] * pow(c[0], float(7))) / float(7)));
      (scale[0] *= -1.0);
      (atan_c[0] += ((scale[0] * pow(c[0], float(9))) / float(9)));
      (scale[0] *= -1.0);
      (atan_c[0] += ((scale[0] * pow(c[0], float(11))) / float(11)));
      (scale[0] *= -1.0);
      result[0] = (((sign[0] * ((M_PI / 2.0) - atan_c[0])) / (2.0 * M_PI)) + 0.5);
    }
    if ((x[0] < 0.0))
      if ((y[0] < 0.0))
        (result[0] -= 0.5);
      else
        if ((y[0] > 0.0))
          (result[0] += 0.5);
  }
  if (((x[1] > epsilon) || (abs(y[1]) > epsilon)))
  {
    if (((x[1] < 0.0) ^^ (y[1] < 0.0)))
    {
      sign[1] = -1.0;
    }
    if ((abs(y[1]) <= abs(x[1])))
    {
      c[1] = abs((y[1] / x[1]));
      (atan_c[1] += ((scale[1] * pow(c[1], float(1))) / float(1)));
      (scale[1] *= -1.0);
      (atan_c[1] += ((scale[1] * pow(c[1], float(3))) / float(3)));
      (scale[1] *= -1.0);
      (atan_c[1] += ((scale[1] * pow(c[1], float(5))) / float(5)));
      (scale[1] *= -1.0);
      (atan_c[1] += ((scale[1] * pow(c[1], float(7))) / float(7)));
      (scale[1] *= -1.0);
      (atan_c[1] += ((scale[1] * pow(c[1], float(9))) / float(9)));
      (scale[1] *= -1.0);
      (atan_c[1] += ((scale[1] * pow(c[1], float(11))) / float(11)));
      (scale[1] *= -1.0);
      result[1] = (((sign[1] * atan_c[1]) / (2.0 * M_PI)) + 0.5);
    }
    else
    {
      c[1] = abs((x[1] / y[1]));
      (atan_c[1] += ((scale[1] * pow(c[1], float(1))) / float(1)));
      (scale[1] *= -1.0);
      (atan_c[1] += ((scale[1] * pow(c[1], float(3))) / float(3)));
      (scale[1] *= -1.0);
      (atan_c[1] += ((scale[1] * pow(c[1], float(5))) / float(5)));
      (scale[1] *= -1.0);
      (atan_c[1] += ((scale[1] * pow(c[1], float(7))) / float(7)));
      (scale[1] *= -1.0);
      (atan_c[1] += ((scale[1] * pow(c[1], float(9))) / float(9)));
      (scale[1] *= -1.0);
      (atan_c[1] += ((scale[1] * pow(c[1], float(11))) / float(11)));
      (scale[1] *= -1.0);
      result[1] = (((sign[1] * ((M_PI / 2.0) - atan_c[1])) / (2.0 * M_PI)) + 0.5);
    }
    if ((x[1] < 0.0))
      if ((y[1] < 0.0))
        (result[1] -= 0.5);
      else
        if ((y[1] > 0.0))
          (result[1] += 0.5);
  }
  color = result;
  gl_Position = (gtf_ModelViewProjectionMatrix * gtf_Vertex);
}

