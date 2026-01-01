precision mediump float;
precision mediump int;

vec4 gtf_Color = vec4(2.0, 2.0, -0.5, -0.5);

vec4 gtf_Vertex = vec4(+2.0, -1.0, 1.0, (false ? (true ? (1.0 / 0.0) : 2.0) : 2.0));

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
  gl_Position = (gtf_ModelViewProjectionMatrix * a);
}

