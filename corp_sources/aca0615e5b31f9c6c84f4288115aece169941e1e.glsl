precision mediump float;
precision mediump int;

vec4 gtf_Color;

vec4 gtf_Vertex = vec4(0.0, (((false ? false : false) ? -0.5 : 1.0) * -1.0), 0.5, 1.0);

uniform mat4 gtf_ModelViewProjectionMatrix;

varying vec4 color;

void main()
{
  const vec2 edge = vec2(0.5, 0.5);
  vec2 c = gtf_Color.rg;
  if ((true ? true : (!false && false)))
  {
    ivec2(2, 0);
  }
  else
  {
    -1.0;
  }
  if ((c[1] >= edge[1]))
  {
    c[1] = 1.0;
  }
  else
  {
    c[1] = 0.0;
  }
  color = vec4(c, 0.0, 1.0);
  gl_Position = (gtf_ModelViewProjectionMatrix * gtf_Vertex);
}

