const int s = int(uint64_t(T1(T2(uint64_t(3)))));
int x[s];
const uint64_t t = uint64_t(true ? T2(uint64_t(10)) : T2(uint64_t(11)));
const uint64_t s2 = sizeof(T1);
uint buf[int(s2)];
void main()
{
    T1 a = T1(uint64_t(4)), b = T1(uint64_t(5));
    T1 c = true ? a : b;
    T1 d = (a,b);
    T1 e = true ? T1(uint64_t(6)) : T1(uint64_t(7));
    T1 f = a.y ? T1(uint64_t(8)) : T1(uint64_t(9));
    f[3].x = 1;
    (f+5).x = 1;
    T1 arr[2] = {a, f};
    arr[1][7].x = 1;
    int i;
    arr[i][i].x = 1;
    arr[i][i][i][i][i][i][i].x = 1;
    T1 j;
    j = j+1;
    j = j-2;
    j += 3;
    j -= 4;
    j = 5+j;
    T1 k = j + 6;
    int64_t x = k - j;
    uint64_t y = sizeof(T1);
    k = k + (-1);
    T2 m;
    m = m+1;
}
