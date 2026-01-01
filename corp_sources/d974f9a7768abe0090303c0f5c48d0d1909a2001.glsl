precision mediump float;
precision mediump int;

vec4 gtf_Color = vec4(0.5, 2.0, 2.0, -1.0);

vec4 gtf_Vertex = vec4((true ? 1.0 : 0.5));

uniform mat4 gtf_ModelViewProjectionMatrix;

varying vec4 color;

void main()
{
  const vec3 edge = vec3(0.5, 0.5, 0.5);
  color = vec4(step(edge, gtf_Color.rgb), 1.0);
  gl_Position = (gtf_Vertex * gtf_ModelViewProjectionMatrix);
}

