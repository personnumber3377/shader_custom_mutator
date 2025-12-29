float4 Fn2(AppendStructuredBuffer<float4> arg_a, ConsumeStructuredBuffer<float4> arg_c)
{
    arg_a.Append(float4(1,2,3,4));
    return arg_c.Consume();
}
AppendStructuredBuffer<float4>  sbuf_a;
ConsumeStructuredBuffer<float4> sbuf_c;
AppendStructuredBuffer<float4>  sbuf_unused;
float4 main(uint pos : FOO) : SV_Target0
{
    return Fn2(sbuf_a, sbuf_c);
}
