void foo()
{
    beginInvocationInterlockARB();
    endInvocationInterlockARB();
}
void main() {
    endInvocationInterlockARB();
    beginInvocationInterlockARB();
    return;
    endInvocationInterlockARB();
}
