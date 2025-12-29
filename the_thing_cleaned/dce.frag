const bool flag = false;
int c = 0;
void bar()
{
    if (flag)
        ++c;
    else
        ++c;
    flag ? ++c : ++c;
    switch (c) {
    case 1:
        ++c;
        break;
        ++c;
    case 2:
        break;
        ++c;
    default:
        break;
    }
    for (int i = 0; i < 0; ++i)
        ++c;
    for (int i = 0; i < 10; ++i) {
        if (c < 3) {
            break;
            ++c;
        } else {
            continue;
            ++c;
        }
    }
    return;
    ++c;
}
int foo()
{
    if (c > 4) {
        return 4;
        ++c;
    }
    return 5;
    ++c;
}
