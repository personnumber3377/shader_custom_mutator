struct foo {
  vec3 a;
  vec2 b;
  float c[100];
};

struct bar {
  foo a;
  foo b;
  foo c;
} a, b, c;

void main()
{
  bar a = 0, b = bar(a.b, foo(vec3(((a || !a) ? a : a), a, -a), vec2(a, a.b), a.c), foo(vec3((a ? a.b : ((a ? a : a) ? a : (a * a))), a.b, a), vec2(a, a), a.a)), c = bar(foo(vec3(--a, b.c, a.a), vec2(-(!b ? (b / b) : (a * b)), (((a && a) || a) ? b : -+a)), (b + (b + +b))), foo(vec3(a.b, -a.c, b.c), vec2(b, (a - (+a - a.a))), (a + a)), foo(vec3(a.b, b.b, (((b && a) ? b.c : !a) ? ((b || b) ? a.b : a.c) : (a ? b : -b))), vec2((((b || a) ? a : b.b) ? ((b / a) * (b * b)) : (a ? a : a)), a.a), b));
}

