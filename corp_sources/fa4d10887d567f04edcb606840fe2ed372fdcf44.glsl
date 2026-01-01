precision mediump float;
precision mediump int;

vec4 gtf_Color = vec4(-1.0, (true ? +0.5 : 2.0), -0.5, -2.0);

vec4 gtf_Vertex;

uniform mat4 gtf_ModelViewProjectionMatrix;

varying vec4 color;

void main()
{
  const vec2 edge = vec2(0.5, 0.5);
  color = vec4(step(edge, gtf_Color.rg), 0.0, 1.0);
  gl_Position = (gtf_ModelViewProjectionMatrix * gtf_Vertex);
}

