precision mediump float;
precision mediump int;

vec4 gtf_Color;

vec4 gtf_Vertex;

uniform mat4 gtf_ModelViewProjectionMatrix;

varying vec4 color;

void main()
{
  vec3 c = ((10.0 * 2.0) * (gtf_Color.rgb - 0.5));
  c = (abs((fract(c) - 0.5)) * 2.0);
  color = vec4(c, 1.0);
  gl_Position = (gtf_ModelViewProjectionMatrix * gtf_Vertex);
}

