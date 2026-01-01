precision mediump float;
precision mediump int;

vec4 gtf_Color;

vec4 gtf_Vertex = vec4(-((1.0 / 0.0) + 2.0), 0.0, 2.0, +((0.0 - 0.0) * (false ? 2.0 : 0.0)));

uniform mat4 gtf_ModelViewProjectionMatrix;

varying vec4 color;

void main()
{
  vec4 lightloc = gtf_Vertex;
  float x = lightloc.x;
  float y = lightloc.y;
  float z = lightloc.z;
  float w = lightloc.w;
  vec4 m = vec4(x, y, z, w);
  color = gtf_Color;
  gl_Position = (gtf_ModelViewProjectionMatrix * m);
}

