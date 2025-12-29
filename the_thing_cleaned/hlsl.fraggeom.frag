struct myVertex {
    float4 pos : SV_Position;
};
[maxvertexcount(1)]
void GS_Draw(point myVertex IN, inout PointStream<myVertex> OutputStream)
{
    OutputStream.Append(IN);
    OutputStream.RestartStrip();
}
float4 main() : SV_TARGET
{
    return 0;
}
