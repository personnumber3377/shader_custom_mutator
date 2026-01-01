precision mediump float;
precision mediump int;

vec4 gtf_Color;

vec4 gtf_Vertex = vec4((false ? 0.0 : -1.0), 1.0, 2.0, (true ? 0.5 : (!false ? 1.0 : (false ? -1.0 : 1.0))));

uniform mat4 gtf_ModelViewProjectionMatrix;

varying vec4 color;

void main()
{
  vec3 c = floor(((10.0 * gtf_Color.rgb) - 4.5));
  vec3 result = vec3(lessThan(ivec3(c), ivec3(0)));
  color = vec4(result, 1.0);
  gl_Position = (gtf_ModelViewProjectionMatrix * gtf_Vertex);
}

