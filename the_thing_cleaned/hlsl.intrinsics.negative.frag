float PixelShaderFunctionS(float inF0, float inF1, float inF2, int inI0)
{
    asdouble(inF0, inF1);
    CheckAccessFullyMapped(3.0);
    countbits(inF0);
    cross(inF0, inF1);
    D3DCOLORtoUBYTE4(inF0);
    determinant(inF0);
    f16tof32(inF0);
    firstbithigh(inF0);
    firstbitlow(inF0);
    length(inF0);
    msad4(inF0, float2(0), float4(0));
    normalize(inF0);
    reflect(inF0, inF1);
    refract(inF0, inF1, inF2);
    refract(float2(0), float2(0), float2(0));
    reversebits(inF0);
    transpose(inF0);
    return 0.0;
}
float1 PixelShaderFunction1(float1 inF0, float1 inF1, float1 inF2, int1 inI0)
{
    GetRenderTargetSamplePosition(inF0);
    return 0.0;
}
float2 PixelShaderFunction2(float2 inF0, float2 inF1, float2 inF2, int2 inI0)
{
    asdouble(inF0, inF1);
    CheckAccessFullyMapped(inF0);
    countbits(inF0);
    cross(inF0, inF1);
    D3DCOLORtoUBYTE4(inF0);
    determinant(inF0);
    f16tof32(inF0);
    firstbithigh(inF0);
    firstbitlow(inF0);
    reversebits(inF0);
    transpose(inF0);
    return float2(1,2);
}
float3 PixelShaderFunction3(float3 inF0, float3 inF1, float3 inF2, int3 inI0)
{
    CheckAccessFullyMapped(inF0);
    countbits(inF0);
    D3DCOLORtoUBYTE4(inF0);
    determinant(inF0);
    f16tof32(inF0);
    firstbithigh(inF0);
    firstbitlow(inF0);
    reversebits(inF0);
    transpose(inF0);
    return float3(1,2,3);
}
float4 PixelShaderFunction(float4 inF0, float4 inF1, float4 inF2, int4 inI0)
{
    CheckAccessFullyMapped(inF0);
    countbits(inF0);
    cross(inF0, inF1);
    determinant(inF0);
    f16tof32(inF0);
    firstbithigh(inF0);
    firstbitlow(inF0);
    reversebits(inF0);
    transpose(inF0);
    return float4(1,2,3,4);
}
    countbits(inF0);          \
    D3DCOLORtoUBYTE4(inF0);   \
    cross(inF0, inF1);        \
    f16tof32(inF0);           \
    firstbithigh(inF0);       \
    firstbitlow(inF0);        \
    reversebits(inF0);        \
    length(inF0);             \
    noise(inF0);              \
    normalize(inF0);          \
    reflect(inF0, inF1);      \
    refract(inF0, inF1, 1.0); \
    reversebits(inF0);        \
float2x2 PixelShaderFunction2x2(float2x2 inF0, float2x2 inF1, float2x2 inF2)
{
    MATFNS()
    return float2x2(2,2,2,2);
}
float3x3 PixelShaderFunction3x3(float3x3 inF0, float3x3 inF1, float3x3 inF2)
{
    MATFNS()
    return float3x3(3,3,3,3,3,3,3,3,3);
}
float4x4 PixelShaderFunction4x4(float4x4 inF0, float4x4 inF1, float4x4 inF2)
{
    MATFNS()
    return float4x4(4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4);
}
