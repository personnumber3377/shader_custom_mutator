precision mediump float;
precision mediump int;

vec4 gtf_Color = vec4(2.0, 0.0, 0.0, 0.0);

vec4 gtf_Vertex;

uniform mat4 gtf_ModelViewProjectionMatrix;

varying vec4 color;

void main()
{
  mat3 m1 = mat3(gtf_Color.rgb, gtf_Color.rgb, gtf_Color.rgb);
  mat3 m2 = mat3(1.0, 0.5, 0.5, 0.5, 1.0, 0.5, 0.5, 0.5, 1.0);
  mat3 m3 = mat3(0.0);
  vec3 result = vec3(0.0, 0.0, 0.0);
  m3 = matrixCompMult(m1, m2);
  (result[0] += m3[0][0]);
  (result[0] += m3[0][1]);
  (result[0] += m3[0][2]);
  (result[1] += m3[1][0]);
  (result[1] += m3[1][1]);
  (result[1] += m3[1][2]);
  (result[2] += m3[2][0]);
  (result[2] += m3[2][1]);
  (result[2] += m3[2][2]);
  color = vec4((result / 2.0), 1.0);
  gl_Position = (gtf_ModelViewProjectionMatrix * gtf_Vertex);
}

