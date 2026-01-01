precision mediump float;
precision mediump int;

vec4 gtf_Color = vec4((false ? -(false ? -1.0 : -1.0) : 0.0), 0.0, +((false || false) ? (false ? 0.0 : 1.0) : (false ? 0.5 : -1.0)), 2.0);

vec4 gtf_Vertex = vec4(0.5, 0.5, -0.5, 2.0);

uniform mat4 gtf_ModelViewProjectionMatrix;

varying vec4 color;

void main()
{
  float v1 = ((gtf_Color.g + 1.0) / 2.0);
  float v2 = ((gtf_Color.b + 1.0) / 2.0);
  color = vec4(((refract(v1, v2, 0.5) + 1.0) / 2.0), 0.0, 0.0, 1.0);
  gl_Position = (gtf_ModelViewProjectionMatrix * gtf_Vertex);
}

