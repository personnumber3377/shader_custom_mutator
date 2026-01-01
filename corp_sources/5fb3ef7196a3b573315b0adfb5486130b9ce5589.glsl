precision mediump float;
precision mediump int;

vec4 gtf_Color = vec4(0.5, 0.0, (0.5 * -1.0), 2.0);

vec4 gtf_Vertex = vec4(2.0, 0.5, ((true ? false : (false ? true : true)) ? -1.0 : 2.0), ((true && true) ? 0.5 : -1.0));

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

