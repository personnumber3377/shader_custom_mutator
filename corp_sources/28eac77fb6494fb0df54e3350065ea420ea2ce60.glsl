precision mediump float;
precision mediump int;

vec4 gtf_Vertex = vec4(-1.0, 0.0, 0.0, ((true ? !true : false) ? (true ? -1.0 : -0.5) : -1.0));

uniform mat4 gtf_ModelViewProjectionMatrix;

uniform mat3 testmat3[2];

varying vec4 color;

void main()
{
  vec3 result = vec3(0.0, 0.0, 0.0);
  for (int j = 0; (j < 3); j++)
  {
    (result += (testmat3[0][j] + testmat3[1][j]));
  }
  color = vec4((result / 2.0), 0.5);
  gl_Position = (gtf_ModelViewProjectionMatrix * gtf_Vertex);
}

