layout(location = 0) in vec4 a0;
layout(location = 1) in vec4 a1;
layout(location = 2) in vec4 a2;
layout(location = 3) in vec4 a3;
layout(location = 0) out vec4 oColor;
void main()
{
    vec4 temp = vec4(1.0);
    if (true)
    {
        temp *= a0;
        temp *= a2;
    }
    if (false)
    {
        temp *= a1;
        temp *= a3;
    }
    oColor = temp;
}
