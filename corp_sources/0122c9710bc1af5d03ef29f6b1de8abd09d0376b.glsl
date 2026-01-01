precision mediump float;
precision mediump int;

attribute vec4 gtf_Vertex;
attribute vec4 gtf_Color;
uniform mat4 gtf_ModelViewProjectionMatrix;
uniform mat4 transforms;
varying vec4 color;
void main()
{
  color = gtf_Color;
   gl_Position = gtf_ModelViewProjectionMatrix* transforms * gtf_Vertex;
}
