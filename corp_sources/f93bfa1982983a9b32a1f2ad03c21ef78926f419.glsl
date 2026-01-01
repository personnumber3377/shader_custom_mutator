precision mediump float;
precision mediump int;

precision mediump float;
uniform mat3 testmat3[2];
varying vec4  color;
void main()
{
     vec3 result = vec3(0.0, 0.0, 0.0);
     result = testmat3[1][0] + testmat3[1][1] + testmat3[1][2];
     gl_FragColor = vec4(result/2.0, 0.5);
}
