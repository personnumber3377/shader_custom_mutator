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
  bar a = bar(foo(vec3(-1.0, 1.0, 0.5), vec2(0.5, 0.0), 0.5), foo(vec3(0.5, 1.0, 0.5), vec2(0.0, 0.0), -1.0), foo(vec3(-0.5, 0.0, 0.5), vec2(0.0, 0.5), 0.0)), b = bar(foo(vec3((false ? -0.0 : -0.5), a.b, 0.5), vec2(-1.0, -1.0), (((true ? false : false) ? 1.0 : (0.0 * 2.0)) + a.b)), foo(vec3(2.0, (--0.5 + a.c), -1.0), vec2(--0.0, a.c), +(-1.0 / (false ? 1.0 : 1.0))), foo(vec3(((+0.0 - 2.0) / 2.0), (!!true ? ((0.5 + 0.5) * 2.0) : (1.0 / 0.0)), (!!false ? (true ? (true ? 1.0 : 0.5) : a.c) : 0.0)), vec2((0.0 - (+0.0 - a.a)), a.c), 0.0)), c = bar(foo(vec3(-1.0, b.b, (((false && true) ? b.c : !true) ? ((false || false) ? a.b : a.c) : (true ? 2.0 : (1.0 - 1.0)))), vec2((((false || true) ? true : b.b) ? ((2.0 / -1.0) * 0.5) : ((false ? -1.0 : 0.0) * a.a)), +a.a), 1.0), foo(vec3((!a.a ? 0.0 : +2.0), 2.0, (((false && false) ? a.c : false) ? ((-1.0 * -1.0) + (2.0 * 0.0)) : ((true ? true : true) ? (true ? 1.0 : 0.0) : 0.0))), vec2(+-(false ? 2.0 : 1.0), 0.0), (!!false ? 2.0 : (-1.0 / b.a))), foo(vec3((a.c + -2.0), ++(-1.0 * 0.5), a.b), vec2(b.c, -1.0), (1.0 - -b.b)));
}

