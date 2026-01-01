precision mediump float;
precision mediump int;

vec4 gtf_Vertex;

vec4 gtf_Color = vec4(1.0, -1.0, 1.0, (-(false ? 0.0 : -1.0) - 1.0));

uniform mat4 gtf_ModelViewProjectionMatrix;

varying vec4 color;

void main()
{
  vec2 c = floor((4.0 * gtf_Color.rg));
  color = vec4(vec3(all(bvec2(c))), 1.0);
  gl_Position = (gtf_ModelViewProjectionMatrix * gtf_Vertex);
}

