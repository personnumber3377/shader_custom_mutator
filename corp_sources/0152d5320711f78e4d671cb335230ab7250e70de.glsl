precision mediump float;
precision mediump int;

vec4 gtf_Color;

vec4 gtf_Vertex;

uniform mat4 gtf_ModelViewProjectionMatrix;

varying vec4 color;

void main()
{
  vec4 lightloc = gtf_Vertex;
  vec3 m = lightloc.rgb;
  vec2 t = m.rg;
  float k = m.b;
  vec4 a = vec4(t, k, lightloc.a);
  color = gtf_Color;
  0.0;
}

