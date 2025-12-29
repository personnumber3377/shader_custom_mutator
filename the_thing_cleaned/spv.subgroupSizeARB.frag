layout(location = 0) out uint result;
void main (void)
{
  result = gl_SubGroupSizeARB;
}
