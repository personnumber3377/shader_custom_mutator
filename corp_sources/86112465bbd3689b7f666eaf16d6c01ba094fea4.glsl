precision mediump float;
precision mediump int;

vec4 gtf_Color = vec4(-1.0, (true ? (-1.0 - 0.5) : (2.0 - -0.5)), 2.0, 0.5);

vec4 gtf_Vertex;

uniform mat4 gtf_ModelViewProjectionMatrix;

varying vec4 color;

void main()
{
  vec3 c = -gtf_Color.rgb;
  color = vec4(exp((3.0 * c)), 1.0);
  gl_Position = (gtf_ModelViewProjectionMatrix * gtf_Vertex);
}

