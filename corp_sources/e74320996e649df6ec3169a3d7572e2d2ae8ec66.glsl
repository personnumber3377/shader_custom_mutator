precision mediump float;
precision mediump int;

precision mediump float;
void main()
{
 int sum =1;
 sum = __LINE__;
 sum = __FILE__;
 sum = __LINE__;
 sum = __FILE__;
 sum = __LINE__ + __FILE__ ;
 sum = __FILE__;
 sum = __VERSION__;
 sum = sum + __LINE__ ;
 sum = __LINE__;
 sum = __FILE__;
 sum = __VERSION__;
}
