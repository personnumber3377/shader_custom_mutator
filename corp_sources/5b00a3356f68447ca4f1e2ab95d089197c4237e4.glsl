precision mediump float;
precision mediump int;

vec4 gtf_Vertex = vec4(0.5, 0.0, (0.5 * -1.0), 2.0);

uniform mat4 gtf_ModelViewProjectionMatrix;

varying vec4 color;

void main()
{
  float x;
  mat3 a = mat3(1.0, 2.0, 4.0, 8.0, 16.0, 32.0, 64.0, 128.0, 256.0);
  mat3 b = a;
  bool elms = true;
  if ((b[0][0] != 1.0))
    elms = false;
  if ((b[0][1] != 2.0))
    elms = false;
  if ((b[0][2] != 4.0))
    elms = false;
  if ((b[1][0] != 8.0))
    elms = false;
  if ((b[1][1] != 16.0))
    elms = false;
  if ((b[1][2] != 32.0))
    elms = false;
  if ((b[2][0] != 64.0))
    elms = false;
  if ((b[2][1] != 128.0))
    elms = false;
  if ((b[2][2] != 256.0))
    elms = false;
  bool rows = true;
  x = ((b[0][0] + b[1][0]) + b[2][0]);
  if (((x < (73.0 - 0.1)) || (x > (73.0 + 0.1))))
    rows = false;
  x = ((b[0][1] + b[1][1]) + b[2][1]);
  if (((x < (146.0 - 0.1)) || (x > (146.0 + 0.1))))
    rows = false;
  x = ((b[0][2] + b[1][2]) + b[2][2]);
  if (((x < (292.0 - 0.1)) || (x > (292.0 + 0.1))))
    rows = false;
  bool cols = true;
  x = ((b[0][0] + b[0][1]) + b[0][2]);
  if (((x < (7.0 - 0.1)) || (x > (7.0 + 0.1))))
    cols = false;
  x = ((b[1][0] + b[1][1]) + b[1][2]);
  if (((x < (56.0 - 0.1)) || (x > (56.0 + 0.1))))
    cols = false;
  x = ((b[2][0] + b[2][1]) + b[2][2]);
  if (((x < (448.0 - 0.1)) || (x > (448.0 + 0.1))))
    cols = false;
  float gray = (((elms && rows) && cols) ? 1.0 : 0.0);
  color = vec4(gray, gray, gray, 1.0);
  gl_Position = (gtf_ModelViewProjectionMatrix * gtf_Vertex);
}

