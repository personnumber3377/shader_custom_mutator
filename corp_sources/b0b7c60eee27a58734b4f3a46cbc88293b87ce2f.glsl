precision mediump float;
precision mediump int;

vec4 gtf_Vertex = vec4(0.5, 0.0, 0.5, 0.0);

uniform mat4 gtf_ModelViewProjectionMatrix;

varying vec4 color;

void main()
{
  int m = 102;
  int k = 12;
  int result = (m / k);
  float gray;
  if (((result == 8) || (result == 9)))
    gray = 1.0;
  else
    gray = 0.0;
  color = vec4(gray, gray, gray, 1.0);
  gl_Position = (gtf_ModelViewProjectionMatrix * gtf_Vertex);
}

