precision mediump float;
precision mediump int;

vec4 gtf_Vertex = vec4(2.0, -1.0, (+1.0 + ((true ? true : true) ? (0.5 / 2.0) : 0.0)), 0.0);

uniform mat4 gtf_ModelViewProjectionMatrix;

varying vec4 color;

void main()
{
  int m = 23;
  int k = --m;
  float gray;
  if (((k == 22) && (m == 22)))
    gray = 1.0;
  else
    gray = 0.0;
  color = vec4(gray, gray, gray, 1.0);
  gl_Position = (gtf_ModelViewProjectionMatrix * gtf_Vertex);
}

