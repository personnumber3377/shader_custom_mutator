struct PS_OUTPUT { float4 color : SV_Target0; };
PS_OUTPUT main()
{
    uint  r01 = 0bERROR321u;
    uint  r02 = 0b11111111111111111111111111111111111111111111111111111111111111111u;
    uint  r03 = 0xTESTu
    uint  r04 = 0xFFFFFFFFFFFFFFFFFFu;
    PS_OUTPUT ps_output;
    ps_output.color = r01;
    return ps_output;
}
