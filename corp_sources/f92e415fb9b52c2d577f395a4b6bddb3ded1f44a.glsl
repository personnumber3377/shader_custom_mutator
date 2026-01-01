precision mediump float;
precision mediump int;

vec4 gtf_Vertex;

vec4 gtf_Color;

uniform mat4 gtf_ModelViewProjectionMatrix;

varying vec4 color;

void main()
{
  const float M_PI = 3.141592653589793;
  float x = (2.0 * (gtf_Color.g - 0.5));
  float y = (2.0 * (gtf_Color.b - 0.5));
  const float epsilon = 0.0001;
  color = vec4(0.0, 0.0, 0.0, 1.0);
  if (((x > epsilon) || (abs(y) > epsilon)))
  {
    color = vec4(((atan(y, x) / (2.0 * M_PI)) + 0.5), 0.0, 0.0, 1.0);
  }
  gtf_Color = (mat4(-1.0, (-1.0 + ((true ? -1.0 : 1.0) - 2.0)), -1.0, (0.0 - (false ? -0.5 : (false ? 2.0 : -1.0))), ((false ? (false ? false : false) : (true && false)) ? (!false ? +-1.0 : 0.0) : +0.0), ((!false ? (true ? 1.0 : 0.0) : 0.0) + 0.0), (-1.0 + ((false && false) ? (false ? 1.0 : -1.0) : +2.0)), 2.0, -1.0, (true ? (false ? 0.0 : (0.5 / 0.0)) : (!true ? -1.0 : +1.0)), 1.0, ((false ? (false ? true : false) : (false || false)) ? 2.0 : 0.0), -1.0, -1.0, 1.0, 2.0) * gtf_Vertex);
}

