precision mediump float;
precision mediump int;

vec4 gtf_Color;

vec4 gtf_Vertex = vec4(-((1.0 / 0.0) + 2.0), 0.0, 2.0, +((0.0 - 0.0) * (false ? 2.0 : 0.0)));

vec4 gtf_MultiTexCoord0;

varying vec4 texCoord[1];

varying vec4 color;

uniform mat4 gtf_ModelViewProjectionMatrix;

void main()
{
  color = gtf_Color;
  texCoord[0] = gtf_MultiTexCoord0;
  gl_Position = (gtf_ModelViewProjectionMatrix * gtf_Vertex);
}

