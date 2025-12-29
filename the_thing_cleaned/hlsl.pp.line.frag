struct PS_OUTPUT
{
    float4 Color : SV_Target0;
    float  Depth : SV_Depth;
};
PS_OUTPUT main()
{
   PS_OUTPUT psout;
   int thisLineIs = __LINE__;
   psout.Color = float4(thisLineIs, 0, 0, 1);
   psout.Depth = 1.0;
   return psout;
}
