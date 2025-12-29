static float g_array [ ] = { 1, 2, 3, 4, 5 };
static float g_array_unused [ ] = { 1, 2, 3, 4, 5, 6, 7 };
static struct mystruct {
    int i;
    float f;
} g_mystruct[] = {
    { 1, 2.0 },
    { 3, 4.0 },
};
struct PS_OUTPUT { float4 color : SV_Target0; };
void main(out PS_OUTPUT ps_output)
{
    float l_array[] = { 1, 2, 3 };
    int idx;
    ps_output.color = g_array[0] + g_array[4] + l_array[1] + g_mystruct[0].f + g_array[idx];
}
