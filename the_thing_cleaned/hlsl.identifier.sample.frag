struct MyStruct {
    sample        float a;
    noperspective float b;
    linear        float c;
    centroid      float d;
};
int sample(int x) { return x; }
float4 main() : SV_Target0
{
    float4 sample = float4(3,4,5,6);
    return sample.rgba;
}
