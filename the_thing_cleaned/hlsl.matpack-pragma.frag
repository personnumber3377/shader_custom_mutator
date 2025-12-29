struct MyBuffer1
{
    column_major float4x4 mat1;
    row_major    float4x4 mat2;
     float4x4 mat3;
};
struct MyBuffer2
{
    column_major float4x4 mat1;
    row_major    float4x4 mat2;
     float4x4 mat3;
};
cbuffer Example
{
    MyBuffer1 g_MyBuffer1;
    MyBuffer2 g_MyBuffer2;
    column_major float4x4 mat1a;
};
float4 main() : SV_Target0
{
    return
        g_MyBuffer1.mat1[0] + g_MyBuffer1.mat2[0] + g_MyBuffer1.mat3[0] +
        g_MyBuffer2.mat1[0] + g_MyBuffer2.mat2[0] + g_MyBuffer2.mat3[0];
}
