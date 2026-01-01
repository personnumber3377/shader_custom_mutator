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
  gl_Position = (mat4(1.0, 0.5, (+1.0 - ((false ? 0.0 : 0.0) + -1.0)), (1.0 - 1.0), +(2.0 + -1.0), -1.0, ((false ? (false || true) : !true) ? -1.0 : 2.0), 2.0, 0.5, +0.5, (((true || false) && (true || false)) ? 0.0 : 0.0), 0.0, (1.0 - -0.0), -1.0, 0.0, 1.0) * gtf_Vertex);
}

