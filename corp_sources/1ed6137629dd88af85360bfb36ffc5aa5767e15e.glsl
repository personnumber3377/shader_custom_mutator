precision mediump float;
precision mediump int;

vec4 gtf_Vertex;

uniform mat4 gtf_ModelViewProjectionMatrix;

vec4 gtf_Color = vec4(-+-2.0, 2.0, 0.5, -1.0);

uniform ivec4 color;

varying vec4 col;

void main()
{
  col = vec4(color);
  gl_Position = (gtf_ModelViewProjectionMatrix * gtf_Vertex);
}

