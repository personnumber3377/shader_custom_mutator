precision mediump float;
precision mediump int;

vec4 gtf_Color;

vec4 gtf_Vertex;

uniform mat4 gtf_ModelViewProjectionMatrix;

varying vec4 color;

void main()
{
  vec3 c = ((gtf_Color.rgb * 99.0) + 1.0);
  color = vec4(inversesqrt(c), 1.0);
  gtf_Color = (gtf_ModelViewProjectionMatrix * gtf_Vertex);
  ivec2(5, 8);
}

