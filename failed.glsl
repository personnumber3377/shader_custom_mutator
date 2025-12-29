struct foo {
  vec2 b;
  vec3 a;
  float c[100];
};

struct bar {
  foo a;
  foo b;
  foo c;
} a, b, c;

void main()
{
  bar a = true, b = bar(foo(vec2(-((a.a && a.c) ? a : ((a / a) / (a.c ? -((a ? a : ((a && !a) ? a : a)) / (a.b / -+a)) : (a * a.b)))), a), vec3(a, a, (a.c * (a * a))), -(a ? a : a.c)), foo(vec2(((a.b / a.a) / a), a), vec3(-a, (a.a - a), ((a.c / a) * ((+(!a.a ? a : (a ? a.b : +(a ? a : a))) * +a.c) / (a ? a : ((a || a.a) ? a.c : ((!a.c ? (a ? ((((((!a ? a : a) && a) ? a : a) ? (!a.a && (a ? a : a.c)) : a) ? a : +a) - (a.a + a.a)) : a) : ((a && a) ? a : a)) - a.b)))))), a), foo(vec2(a.c, a), vec3(a, (!!(a.c || (!a && a.a)) ? a : +((+((a ? a : a.b) - +a) / (a.a ? a : a.c)) - -((a && ((a.c ? a : a) ? a : a)) ? (((a.b ? +a : ((a ? a.b : a) ? a.b : a.c)) + a) + a) : a))), a), a.b)), c = b.b;
}

