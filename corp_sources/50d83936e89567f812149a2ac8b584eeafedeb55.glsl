precision mediump float;
precision mediump int;

vec4 gtf_Color;

vec4 gtf_Vertex;

uniform mat4 gtf_ModelViewProjectionMatrix;

varying vec4 color;

float ceil_ref(float x)
{
  if ((x != floor(x)))
    x = (floor(x) + 1.0);
  return x;
}

void main()
{
  float c = (ceil_ref(ceil_ref(0.5)) * (0.5 - gtf_Color.r));
  color = vec4(((ceil_ref(c) + 10.0) / 20.0), 0.0, 0.0, 1.0);
  gl_Position = (gtf_ModelViewProjectionMatrix * gtf_Vertex);
}

