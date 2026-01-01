precision mediump float;
precision mediump int;

vec4 gtf_Color;

vec4 gtf_Vertex = vec4(0.0, (((false ? false : false) ? -0.5 : 1.0) * -1.0), 0.5, 1.0);

uniform mat4 gtf_ModelViewProjectionMatrix;

varying vec4 color;

void main()
{
  vec3 c = ((gtf_Color.rgb * 99.0) + 1.0);
  color = vec4(inversesqrt(c), 1.0);
  gl_Position = (gtf_ModelViewProjectionMatrix * gtf_Vertex);
  ivec2(5, 8);
}

