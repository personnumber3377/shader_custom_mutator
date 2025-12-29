float a2;
float f;
float bar();
out float cout;
in float cin;
float foo()
{
    float h2 = 2 * f + cin;
    float g2 = bar();
    return h2 + g2 + gl_FragCoord.y;
}
