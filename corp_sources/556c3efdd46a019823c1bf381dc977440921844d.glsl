precision mediump float;
precision mediump int;

vec4 gtf_Vertex = vec4(-((false ? false : false) ? +1.0 : 2.0), (((false || true) ? (true ? 2.0 : 2.0) : +-1.0) - -0.5), 1.0, (true ? 0.0 : 0.0));

varying vec4 color;

vec4 gtf_Color = vec4(0.0, 2.0, -0.5, 1.0);

uniform mat4 gtf_ModelViewProjectionMatrix;

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
  gl_Position = (gtf_ModelViewProjectionMatrix * gtf_Vertex);
}

