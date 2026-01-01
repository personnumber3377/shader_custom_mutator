precision mediump float;
precision mediump int;

vec4 gtf_Vertex = vec4(+0.0, -1.0, (-1.0 + 0.5), 2.0);

uniform mat4 gtf_ModelViewProjectionMatrix;

varying vec4 color;

void main()
{
  mat3 m = mat3(0.5);
  vec4 black = vec4(0.0, 0.0, 0.0, 1.0);
  vec4 result = vec4(1.0, 1.0, 1.0, 1.0);
  if ((m[0][0] != 0.5))
    result = black;
  if ((m[0][1] != 0.0))
    result = black;
  if ((m[0][2] != 0.0))
    result = black;
  if ((m[1][0] != 0.0))
    result = black;
  if ((m[1][1] != 0.5))
    result = black;
  if ((m[1][2] != 0.0))
    result = black;
  if ((m[2][0] != 0.0))
    result = black;
  if ((m[2][1] != 0.0))
    result = black;
  if ((m[2][2] != 0.5))
    result = black;
  color = result;
  gl_Position = (gtf_ModelViewProjectionMatrix * gtf_Vertex);
}

