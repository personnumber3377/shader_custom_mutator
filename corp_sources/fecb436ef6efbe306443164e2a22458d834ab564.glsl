precision mediump float;
precision mediump int;

vec4 gtf_Color = vec4(2.0, 1.0, 0.5, 0.5);

vec4 gtf_Vertex = vec4(0.5, +2.0, 0.5, 0.0);

uniform mat4 gtf_ModelViewProjectionMatrix;

varying vec4 color;

void main()
{
  color = vec4(vec3(length(gtf_Color.r)), 1.0);
  gl_Position = (gtf_ModelViewProjectionMatrix * gtf_Vertex);
}

