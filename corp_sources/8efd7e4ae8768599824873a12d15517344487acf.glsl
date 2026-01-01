precision mediump float;
precision mediump int;

vec4 gtf_Color = vec4((0.0 / 0.5), +0.5, 1.0, 1.0);

vec4 gtf_Vertex;

uniform mat4 gtf_ModelViewProjectionMatrix;

varying vec4 color;

void main()
{
  const vec3 max_c = vec3(0.5, 0.5, 0.5);
  vec3 c = gtf_Color.rgb;
  if ((c[0] < max_c[0]))
    c[0] = max_c[0];
  if ((c[1] < max_c[1]))
    c[1] = max_c[1];
  if ((c[2] < max_c[2]))
    c[2] = max_c[2];
  color = vec4(c, 1.0);
  gl_Position = (gtf_ModelViewProjectionMatrix * gtf_Vertex);
}

