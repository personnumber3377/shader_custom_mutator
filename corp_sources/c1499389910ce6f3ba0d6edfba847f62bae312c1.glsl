precision mediump float;
precision mediump int;

attribute vec4 gtf_Normal;
uniform mat4 gtf_NormalMatrix;
void main()
{
   vec4 v = vec4(1,2,3,4);
   vec3 v3 = vec3(5,6,7);
   vec4 v4  = vec4(normalize(v3.yzy).xyz.zyx, 1.0);
   gl_Position = v4 + vec4(normalize(gtf_NormalMatrix * gtf_Normal).xyz.zyx, v4.y);
}
