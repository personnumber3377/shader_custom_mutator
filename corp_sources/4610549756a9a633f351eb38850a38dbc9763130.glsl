precision mediump float;
precision mediump int;

precision mediump float;
uniform vec3 lightPosition;
varying vec4  color;
void main()
{
     gl_FragColor = vec4(lightPosition, 0.0);
}
