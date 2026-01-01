precision mediump float;
precision mediump int;

vec4 gtf_Vertex = vec4(2.0, 0.0, 0.0, 0.0);

vec4 gtf_Color = vec4(0.0, ((true || (false && true)) ? 1.0 : (1.0 * (false ? 0.5 : -1.0))), +1.0, +-(false ? 2.0 : 0.0));

uniform mat4 gtf_ModelViewProjectionMatrix;

varying vec4 color;

void main()
{
  color = gtf_Color;
  gl_PointSize = 20.0;
  gl_Position = (gtf_ModelViewProjectionMatrix * gtf_Vertex);
  vec4(1.0, -1.0, +1.0, +0.5);
}

