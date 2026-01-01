precision mediump float;
precision mediump int;

vec4 gtf_Color;

vec4 gtf_Vertex = vec4((false ? 1.0 : (0.0 - 0.5)), 0.0, (false ? (0.5 + 0.5) : 1.0), +((false ? 1.0 : 2.0) + 1.0));

uniform mat4 gtf_ModelViewProjectionMatrix;

varying vec4 color;

void main()
{
  const float M_PI = 3.141592653589793;
  vec3 v1;
  vec3 v2 = normalize(vec3(1.0, 1.0, 1.0));
  float theta = ((gtf_Color.g * 2.0) * M_PI);
  float phi = ((gtf_Color.b * 2.0) * M_PI);
  v1.x = (cos(theta) * sin(phi));
  v1.y = (sin(theta) * sin(phi));
  v1.z = cos(phi);
  color = vec4((((v1 - ((2.0 * dot(v2, v1)) * v2)) + vec3(1.0)) / 2.0), 1.0);
  gl_Position = (gtf_ModelViewProjectionMatrix * gtf_Vertex);
}

