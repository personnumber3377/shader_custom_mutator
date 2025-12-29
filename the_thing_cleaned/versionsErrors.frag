attribute vec3 color;
uniform sampler2DRect foo;
void main()
{
    gl_FragColor = vec4(color, 142.0f);
    discard;
}
