struct Nested { float y; Texture2D texNested; };
struct A { Nested n; float x; };
struct B { Nested n; Texture2D tex; };
Texture2D someTex;
float4 main(float4 vpos : VPOS) : COLOR0
{
    A a1, a2;
    B b;
    a1.n = a2.n;
    b .n = a1.n;
    Nested n = b.n;
    a2.n.texNested = someTex;
    a1.n.y = 1.0;
    return float4(0,0,0,0);
}
