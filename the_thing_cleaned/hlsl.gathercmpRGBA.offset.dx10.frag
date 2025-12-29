SamplerComparisonState g_sSampCmp : register(s0);
Texture1D          g_tTex1df4a : register(t1);
uniform Texture1D <float4> g_tTex1df4 : register(t0);
Texture1D <int4>   g_tTex1di4;
Texture1D <uint4>  g_tTex1du4;
Texture2D <float4> g_tTex2df4;
Texture2D <int4>   g_tTex2di4;
Texture2D <uint4>  g_tTex2du4;
Texture3D <float4> g_tTex3df4;
Texture3D <int4>   g_tTex3di4;
Texture3D <uint4>  g_tTex3du4;
TextureCube <float4> g_tTexcdf4;
TextureCube <int4>   g_tTexcdi4;
TextureCube <uint4>  g_tTexcdu4;
struct PS_OUTPUT
{
    float4 Color : SV_Target0;
    float  Depth : SV_Depth;
};
uniform float  c1;
uniform float2 c2;
uniform float3 c3;
uniform float4 c4;
PS_OUTPUT main()
{
   PS_OUTPUT psout;
   uint status;
   float4 txval001 = g_tTex2df4 . GatherCmpRed(g_sSampCmp, c2, 0.75, int2(1,0));
   int4   txval011 = g_tTex2di4 . GatherCmpRed(g_sSampCmp, c2, 0.75, int2(1,-1));
   uint4  txval021 = g_tTex2du4 . GatherCmpRed(g_sSampCmp, c2, 0.75, int2(1,1));
   float4 txval004 = g_tTex2df4 . GatherCmpRed(g_sSampCmp, c2, 0.75, int2(1,0), int2(1,0), int2(1,0), int2(1,0));
   int4   txval014 = g_tTex2di4 . GatherCmpRed(g_sSampCmp, c2, 0.75, int2(1,-1), int2(1,-1), int2(1,-1), int2(1,-1));
   uint4  txval024 = g_tTex2du4 . GatherCmpRed(g_sSampCmp, c2, 0.75, int2(1,1), int2(1,1), int2(1,1), int2(1,1));
   float4 txval401 = g_tTex2df4 . GatherCmp(g_sSampCmp, c2, 0.75, int2(1,0));
   int4   txval411 = g_tTex2di4 . GatherCmp(g_sSampCmp, c2, 0.75, int2(1,-1));
   uint4  txval421 = g_tTex2du4 . GatherCmp(g_sSampCmp, c2, 0.75, int2(1,1));
   psout.Color = 1.0;
   psout.Depth = 1.0;
   return psout;
}
