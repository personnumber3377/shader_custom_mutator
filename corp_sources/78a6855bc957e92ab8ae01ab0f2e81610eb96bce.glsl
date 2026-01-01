precision mediump float;
precision mediump int;

attribute vec4 gtf_Vertex;
uniform mat4 gtf_ModelViewProjectionMatrix;
uniform mat3 testmat3[2];
varying vec4  color;
void main()
{
     vec3 result = vec3(0.0, 0.0, 0.0);
     result = testmat3[1][0] + testmat3[1][1] + testmat3[1][2];
     color = vec4(result/2.0, 0.5);
     gl_Position     = gtf_ModelViewProjectionMatrix * gtf_Vertex;
}
