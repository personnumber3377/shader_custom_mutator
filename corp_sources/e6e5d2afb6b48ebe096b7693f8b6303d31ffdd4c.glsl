precision mediump float;
precision mediump int;

attribute vec4 gtf_Vertex;
uniform mat4 gtf_ModelViewProjectionMatrix;
uniform vec3 lightPosition[2];
varying vec4  color;
void main()
{
     color = vec4(0.0);
     for (int i = 0; i < 2; i++)
     {
          color += vec4(lightPosition[i], 0.0);
     }
     color /= 2.0;
     gl_Position     = gtf_ModelViewProjectionMatrix * gtf_Vertex;
}
