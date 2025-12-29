float4 main() : SV_Target
{
    float f1a;
    float1 f1b;
    f1a = f1b;
    f1b = f1a;
    float3 f3;
    step(0.0, f3);
    sin(f1b);
    return float4(0,0,0,0);
}
