struct T {
    float f : packoffset(c4.y);
    centroid float g;
    float d: SV_DepthGreaterEqual;
    float4 normal;
};
T s;
cbuffer buff {
    T t : packoffset(c5.z);
};
T main(T t : myInput) : SV_Target0
{
    T local;
    return local;
}
