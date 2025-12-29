cbuffer Matrix
{
    float4x4  m44;
    float4x3  m43;
    float3x4  m34;
    float3x3  m33;
    float2x4  m24;
    float4x2  m42;
    float4    v4;
    float3    v3;
    float2    v2;
}
float4 main() : SV_Target0
{
    float  r00 = mul(v2, v3);
    float  r01 = mul(v4, v2);
    float4 r10 = mul(v3, m44);
    float4 r11 = mul(v4, m34);
    float4 r20 = mul(m44, v3);
    float4 r21 = mul(m43, v4);
    float2x3 r30 = mul(m24, m33);
    float3x4 r31 = mul(m33, m24);
    float3x2 r32 = mul(m33, m42);
    float4x3 r33 = mul(m42, m33);
    return r10 + r11 + r20 + r21 + r00 + r01 + r30[0].x + r31[0] + r32[0].x + transpose(r33)[0];
}
