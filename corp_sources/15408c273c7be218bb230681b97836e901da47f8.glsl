precision mediump float;
precision mediump int;

vec4 gtf_Color = vec4(0.5, -1.0, 0.0, (((true || false) ? +0.0 : 0.5) + ((true ? true : true) ? -1.0 : 1.0)));

vec4 gtf_Vertex;

uniform mat4 gtf_ModelViewProjectionMatrix;

varying vec4 color;

void main()
{
  color = vec4(vec3(sqrt(pow(abs((gtf_Color.r - 0.5)), 2.0))), 1.0);
  gtf_Vertex = (gtf_ModelViewProjectionMatrix * gtf_Vertex);
}

