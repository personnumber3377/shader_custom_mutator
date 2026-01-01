precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
uniform vec3 lightPosition[2];
void main()
{
    vec3 v[2];
    v[1] = vec3(color.r, color.g, color.b);
    v[0] = lightPosition[1];
    gl_FragColor =  vec4(v[1] + v[1], 0.0)/2.0;
}
