precision mediump float;
precision mediump int;

vec4 gtf_Color = (false ? vec4(0.0, +2.0, -1.0, (false ? (false ? -1.0 : (true ? 1.0 : 1.0)) : -1.0)) : vec4(-1.0, 0.0, 0.5, -1.0));

vec4 gtf_Vertex = vec4(-1.0, (false ? (+2.0 + -1.0) : 0.5), -1.0, -0.5);

uniform mat4 gtf_ModelViewProjectionMatrix;

varying vec4 color;

void main()
{
  vec4 lightloc = gtf_Vertex;
  vec3 m = lightloc.stp;
  vec4 a = vec4(m.stp, lightloc.q);
  color = gtf_Color;
  gl_Position = (gtf_ModelViewProjectionMatrix * a);
}

