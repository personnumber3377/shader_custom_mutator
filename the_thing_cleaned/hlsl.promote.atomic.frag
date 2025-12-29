RWBuffer<uint> s_uintbuff;
float4 main() : SV_Target
{
    int Loc;
    int Inc;
    int Orig;
    InterlockedAdd(s_uintbuff[Loc], Inc, Orig);
    return float4(0,0,0,0);
}
