precision highp float;
out vec4 my_FragColor;
void main()
{
    float correct = isinf(1.0e2147483649) ? 1.0 : 0.0;
    my_FragColor = vec4(0.0, correct, 0.0, 1.0);
}
