precision mediump float;
precision mediump int;

vec4 gtf_Vertex = vec4((+2.0 / 1.0), 2.0, 0.5, -1.0);

uniform mat4 gtf_ModelViewProjectionMatrix;

varying vec4 color;

const int array_size = 2;

uniform float new_mad2[array_size];

void main()
{
  int i = 0;
  float new_mad[array_size];
  float gray = 0.0;
  new_mad[0] = new_mad2[0];
  new_mad[1] = new_mad2[1];
  if (((new_mad[0] == 45.0) && (new_mad[1] == 14.0)))
    gray = 1.0;
  else
    gray = 0.0;
  color = vec4(gray, gray, gray, 1.0);
  gl_Position = (gtf_ModelViewProjectionMatrix * gtf_Vertex);
}

