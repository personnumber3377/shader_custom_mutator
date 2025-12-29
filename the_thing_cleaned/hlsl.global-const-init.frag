cbuffer CB {
    float4 foo;
};
static const float4 bar = foo;
static const float2 a1[2] = { { 1, 2 }, { foo.x, 4 } };
static const float2 a2[2] = { { 5, 6 }, { 7, 8 } };
float4 main() : SV_Target0
{
    return bar;
}
