SamplerState       g_sSamp : register(s0);
RWTexture1D <float> g_tTex1df1;
RWTexture1D <int>   g_tTex1di1;
RWTexture1D <uint>  g_tTex1du1;
RWTexture2D <float> g_tTex2df1;
RWTexture2D <int>   g_tTex2di1;
RWTexture2D <uint>  g_tTex2du1;
RWTexture3D <float> g_tTex3df1;
RWTexture3D <int>   g_tTex3di1;
RWTexture3D <uint>  g_tTex3du1;
RWTexture1DArray <float> g_tTex1df1a;
RWTexture1DArray <int>   g_tTex1di1a;
RWTexture1DArray <uint>  g_tTex1du1a;
RWTexture2DArray <float> g_tTex2df1a;
RWTexture2DArray <int>   g_tTex2di1a;
RWTexture2DArray <uint>  g_tTex2du1a;
struct PS_OUTPUT
{
    float4 Color : SV_Target0;
};
uniform int   c1;
uniform int2  c2;
uniform int3  c3;
uniform int4  c4;
uniform int   o1;
uniform int2  o2;
uniform int3  o3;
uniform int4  o4;
uniform float uf1;
uniform int   ui1;
uniform uint  uu1;
int   Fn1(in int x)   { return x; }
uint  Fn1(in uint x)  { return x; }
float Fn1(in float x) { return x; }
void Fn2(out int x)   { x = int(0); }
void Fn2(out uint x)  { x = uint(0); }
void Fn2(out float x) { x = float(0); }
float SomeValue() { return c1; }
PS_OUTPUT main()
{
   PS_OUTPUT psout;
   g_tTex1df1[c1];
   float r00 = g_tTex1df1[c1];
   int   r01 = g_tTex1di1[c1];
   uint  r02 = g_tTex1du1[c1];
   float r10 = g_tTex2df1[c2];
   int   r11 = g_tTex2di1[c2];
   uint  r12 = g_tTex2du1[c2];
   float r20 = g_tTex3df1[c3];
   int   r21 = g_tTex3di1[c3];
   uint  r22 = g_tTex3du1[c3];
   float lf1 = uf1;
   g_tTex1df1[c1] = SomeValue();
   g_tTex1df1[c1] = lf1;
   g_tTex1di1[c1] = int(2);
   g_tTex1du1[c1] = uint(3);
   float val1 = (g_tTex1df1[c1] *= 2.0);
   g_tTex1df1[c1] -= 3.0;
   g_tTex1df1[c1] += 4.0;
   g_tTex1di1[c1] /= 2;
   g_tTex1di1[c1] %= 2;
   g_tTex1di1[c1] &= 0xffff;
   g_tTex1di1[c1] |= 0xf0f0;
   g_tTex1di1[c1] <<= 2;
   g_tTex1di1[c1] >>= 2;
   g_tTex2df1[c2] = SomeValue();
   g_tTex2df1[c2] = lf1;
   g_tTex2di1[c2] = int(5);
   g_tTex2du1[c2] = uint(6);
   g_tTex3df1[c3] = SomeValue();
   g_tTex3df1[c3] = lf1;
   g_tTex3di1[c3] = int(8);
   g_tTex3du1[c3] = uint(9);
   Fn1(g_tTex1df1[c1]);
   Fn1(g_tTex1di1[c1]);
   Fn1(g_tTex1du1[c1]);
   Fn2(g_tTex1df1[c1]);
   Fn2(g_tTex1di1[c1]);
   Fn2(g_tTex1du1[c1]);
   ++g_tTex1df1[c1];
   ++g_tTex1di1[c1];
   ++g_tTex1du1[c1];
   --g_tTex1df1[c1];
   --g_tTex1di1[c1];
   --g_tTex1du1[c1];
   g_tTex1df1[c1]++;
   g_tTex1du1[c1]--;
   g_tTex1di1[c1]++;
   g_tTex1df1[c1]--;
   g_tTex1di1[c1]++;
   g_tTex1du1[c1]--;
   g_tTex1df1[1] = g_tTex2df1[int2(2, 3)];
   psout.Color = 1.0;
   return psout;
}
