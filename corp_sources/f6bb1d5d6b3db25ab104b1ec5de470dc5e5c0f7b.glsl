precision mediump float;
precision mediump int;

vec4 gtf_Color = (!(true ? false : true) ? vec4(((!true ? (true ? -1.0 : 0.5) : -1.0) * (2.0 * 0.0)), 2.0, 2.0, 0.0) : vec4(-1.0, (!!false ? -1.0 : 1.0), (true ? 2.0 : (1.0 - +0.5)), 2.0));

vec4 gtf_Vertex;

uniform mat4 gtf_ModelViewProjectionMatrix;

varying vec4 gtf_TexCoord[1];

vec4 gtf_MultiTexCoord0;

varying vec4 color;

void main()
{
  color = gtf_Color;
  gtf_TexCoord[0] = gtf_MultiTexCoord0;
  gl_Position = (gtf_ModelViewProjectionMatrix * gtf_MultiTexCoord0);
  gl_PointSize = 1.0;
}

