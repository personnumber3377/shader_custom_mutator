precision mediump float;
precision mediump int;

vec4 gtf_Color = vec4(0.5, 0.5, 0.0, -0.5);

vec4 gtf_Vertex;

uniform mat4 gtf_ModelViewProjectionMatrix;

varying vec4 color;

void main()
{
  const float edge = 0.5;
  float c = gtf_Color.r;
  if ((c >= edge))
    c = 1.0;
  else
    c = 0.0;
  color = vec4(c, 0.0, 0.0, 1.0);
  gl_Position = (gtf_ModelViewProjectionMatrix * gtf_Vertex);
}

