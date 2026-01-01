precision mediump float;
precision mediump int;

attribute vec4 gtf_Vertex;
uniform mat4 gtf_ModelViewProjectionMatrix;
uniform vec3 lightPosition;
varying vec4  color;
void main()
{
     color              = vec4(lightPosition, 0.0);
     gl_Position     = gtf_ModelViewProjectionMatrix * gtf_Vertex;
}
