precision mediump float;
precision mediump int;

vec4 gtf_Vertex;

vec3 gtf_Normal = vec3(1.0, 2.0, -0.5);

float myAttrib1f;

vec2 myAttrib2f;

vec3 myAttrib3f;

vec4 myAttrib4f;

uniform mat3 gtf_NormalMatrix;

varying float lightIntensity;

varying vec3 Position;

uniform vec3 LightPosition;

uniform mat4 gtf_ModelViewMatrix;

uniform mat4 gtf_ModelViewProjectionMatrix;

const float specularContribution = 0.7;

const float diffuseContribution = (1.0 - specularContribution);

void main()
{
  vec4 pos = (gtf_ModelViewMatrix * gtf_Vertex);
  Position = vec3(gtf_Vertex);
  vec3 tnorm = normalize((gtf_NormalMatrix * gtf_Normal));
  vec3 lightVec = normalize((LightPosition - vec3(pos)));
  vec3 reflectVec = reflect(lightVec, tnorm);
  vec3 viewVec = normalize(vec3(pos));
  float f = (((myAttrib1f + myAttrib2f[0]) + myAttrib3f[0]) + myAttrib4f[0]);
  float spec = clamp(dot(reflectVec, viewVec), f, 1.0);
  spec = (spec * spec);
  spec = (spec * spec);
  spec = (spec * spec);
  spec = (spec * spec);
  lightIntensity = ((diffuseContribution * dot(lightVec, tnorm)) + (specularContribution * spec));
  gl_Position = (gtf_ModelViewProjectionMatrix * gtf_Vertex);
}

