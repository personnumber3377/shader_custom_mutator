float4 main() : SV_Target0
{
    [unroll(5) ] for (int x=0; x<5; ++x);
    [loop] for (int y=0; y<5; ++y);
    for (int z=0; z<5; ++z);
    return 0;
}
