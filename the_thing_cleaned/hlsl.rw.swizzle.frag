RWTexture2D<float3> rwtx;
RWBuffer<float3> buf;
float3 SomeValue() { return float3(1,2,3); }
float4 main() : SV_Target0
{
    int2 tc2 = { 0, 0 };
    int tc = 0;
    rwtx[tc2].zyx = float3(1,2,3);
    rwtx[tc2].zyx = SomeValue();
    rwtx[tc2].zyx = 2;
    return 0.0;
}
