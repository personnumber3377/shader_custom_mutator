struct S {
    float f;
    vec4 v;
};
in S s;
void main()
{
    interpolateAtCentroid(s.v);
    bool b1;
    b1 = anyInvocation(b1);
    b1 = allInvocations(b1);
    b1 = allInvocationsEqual(b1);
}
void attExtBad()
{
    [[dependency_length(1+3)]] for (int i = 0; i < 8; ++i) { }
    [[flatten]]                if (true) { } else { }
}
void attExt()
{
    [[dependency_length(-3)]] do {  } while(true);
    [[dependency_length(0)]] do {  } while(true);
}
