struct A
{
    float4 a EMP1({1,2,3,4});
    float4 b EMP2({({{(({1,2,3,4}))}})}, {{1,2,3,4}});
    float4 c EXP1({1,2,3,4});
    float4 d EXP2({({{(({1,2,3,4}))}})}, {{1,2,3,4}});
};
void main()
{
    "a string"
}
