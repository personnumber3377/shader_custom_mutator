in highp vec3 color;
out highp vec4 foo;
uniform highp sampler2DArrayShadow bar;
void main()
{
    foo = vec4(color, 142.0f);
    discard;
}
