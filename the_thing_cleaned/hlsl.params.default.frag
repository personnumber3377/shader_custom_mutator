uniform int4 ui4;
static const int cia = -4;
static const int cib = -42;
int4 fn1(int4 p0, bool b1, bool b2 = false) {
    return p0;
}
int4 fn1(int4 p0,
         int4 p1    : FOO = int4(-1,-2,-3, cia),
         int  p2[2] : BAR = { int(1), 2 },
         int  p3          = abs(cib) )
{
    return p0 + p1 + p2[0] + p3;
}
int4 fn2(int4 p0, int x = 3)
{
    return int4(10,11,12,13);
}
int4 fn2(int4 p0, float x = sin(3.3))
{
    return p0 + int4(20,21,22,23);
}
void fn3(int p0 = 3) { }
int4 main() : SV_Target0
{
    int myarray[2] = {30,31};
    fn3();
    fn3(5);
    return fn1(100) +
           fn1(101, ui4) +
           fn1(102, ui4, myarray) +
           fn1(103, ui4, myarray, 99) +
           fn1(104, false) +
           fn1(105, false, true) +
           fn2(110, 11.11) +
           fn2(111, 12);
}
