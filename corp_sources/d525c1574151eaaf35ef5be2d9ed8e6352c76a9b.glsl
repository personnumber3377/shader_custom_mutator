precision mediump float;
precision mediump int;

vec4 gtf_Color;

vec4 gtf_Vertex = vec4((false ? 0.0 : -1.0), 1.0, 2.0, (true ? 0.5 : (!false ? 1.0 : (false ? -1.0 : 1.0))));

uniform mat4 gtf_ModelViewProjectionMatrix;

varying vec4 color;

void main()
{
  mat2 m1 = mat2(gtf_Color.r, gtf_Color.g, gtf_Color.b, gtf_Color.a);
  mat2 m2 = mat2(1.0, 0.5, 0.5, 1.0);
  mat2 m3 = mat2(0.0);
  m3[0][0] = (m1[0][0] * m2[0][0]);
  m3[0][1] = (m1[0][1] * m2[0][1]);
  m3[1][0] = (m1[1][0] * m2[1][0]);
  m3[1][1] = (m1[1][1] * m2[1][1]);
  color = vec4(m3[0][0], m3[1][0], m3[0][1], m3[1][1]);
  gl_Position = (gtf_ModelViewProjectionMatrix * gtf_Vertex);
}

