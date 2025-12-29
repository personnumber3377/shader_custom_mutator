struct PS_OUTPUT { float4 color : SV_Target0; };
PS_OUTPUT main()
{
    float r00 = 1.0f;
    uint  r01 = 1u;
    uint  r02 = 2U;
    uint  r03 = 0xabcu;
    uint  r04 = 0XABCU;
    int   r05 = 5l;
    int   r06 = 6L;
    int   r07 = 071;
    uint  r08 = 072u;
    float r09 = 1.h;
    float r10 = 1.H;
    float r11 = 1.1h;
    float r12 = 1.1H;
    uint  r13 = 0b00001u;
    uint  r14 = 0B00010U;
    int   r15 = 0b00011;
    int   r16 = 0B00100;
    uint  r17 = BIN_UINT;
    int   r18 = BIN_INT;
    PS_OUTPUT ps_output;
    ps_output.color = r07;
    return ps_output;
}
