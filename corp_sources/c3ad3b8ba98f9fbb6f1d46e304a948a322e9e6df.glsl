precision mediump float;
precision mediump int;

vec4 gtf_Vertex = vec4(2.0, -1.0, (+1.0 + ((true ? true : true) ? (0.5 / 2.0) : 0.0)), 0.0);

vec4 gtf_Color;

uniform mat4 gtf_ModelViewProjectionMatrix;

uniform mat4 transforms;

varying vec4 color;

void main()
{
  color = gtf_Color;
  gl_Position = ((gtf_ModelViewProjectionMatrix * transforms) * gtf_Vertex);
}

