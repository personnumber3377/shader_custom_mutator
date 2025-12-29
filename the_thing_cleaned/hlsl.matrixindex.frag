uniform int      idx;
uniform float3x2 um;
struct PS_OUTPUT
{
    float4 Color : SV_Target0;
};
PS_OUTPUT main()
{
    const float3x2 m1 = { { 10, 11 },
                          { 12, 13 },
                          { 14, 15 } };
    const float3x2 m2 = { 20, 21, 22, 23, 24, 25 };
    const float3x2 m3 = { 30, 31, 33, 33, 34, 35 };
    float e1_00 = m1[0][0];
    float e1_01 = m1[0][1];
    float e1_10 = m1[1][0];
    float e1_11 = m1[1][1];
    float e1_20 = m1[2][0];
    float e1_21 = m1[2][1];
    float e2_00 = m2[0][0];
    float e2_01 = m2[0][1];
    float e2_10 = m2[1][0];
    float e2_11 = m2[1][1];
    float e2_20 = m2[2][0];
    float e2_21 = m2[2][1];
    float2 r0a = m1[0];
    float2 r1a = m1[1];
    float2 r2a = m1[2];
    float2 r0b = m2[idx];
    float2 r0c = um[idx];
    PS_OUTPUT psout;
    psout.Color = e2_11;
    return psout;
}
