precision mediump float;
precision mediump int;

vec4 gtf_Vertex;

uniform mat4 gtf_ModelViewProjectionMatrix;

uniform vec3 lightPosition[2];

varying vec4 color;

void main()
{
  color = (vec4((lightPosition[0] + lightPosition[1]), 0.0) * 0.5);
  gl_Position = (gtf_ModelViewProjectionMatrix * vec4(-(false ? (false ? 0.5 : 1.0) : 0.5), (2.0 + -0.0), (((true && false) ? (0.0 / -1.0) : 1.0) * +(true ? 1.0 : 1.0)), -1.0));
}

