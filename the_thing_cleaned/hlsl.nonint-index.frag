static const float array[3] = { 1, 2, 3 };
float main(float input : IN) : SV_Target0
{
    return array[input] + array[2.0] + array[true] + array[false];
}
