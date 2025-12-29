struct S { mat4 m; };
buffer blockName { S s1; };
S s2;
void fooConst(const in S s) { }
void foo(in S s) { }
void fooOut(inout S s) { }
void main()
{
  fooConst(s1);
  fooConst(s2);
  foo(s1);
  foo(s2);
  fooOut(s1);
  fooOut(s2);
}
