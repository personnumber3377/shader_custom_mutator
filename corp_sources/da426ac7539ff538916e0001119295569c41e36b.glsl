precision mediump float;
precision mediump int;

vec4 gtf_Color;

vec4 gtf_Vertex;

uniform mat4 gtf_ModelViewProjectionMatrix;

varying vec4 color;

void main()
{
  vec3 c = (0.5 + (gtf_Color.rgb * 99.0));
  color = vec4((1.0 / sqrt(c)), 1.0);
  gl_Position = (gtf_ModelViewProjectionMatrix * gtf_Vertex);
}

