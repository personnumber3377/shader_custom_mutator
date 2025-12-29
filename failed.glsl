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
  bar a = bar(foo(vec3(0.0, 0.5, 0.0), vec2((-(1.0 - 0.5) / 2.0), (+-0.0 / 1.0)), +(false ? +2.0 : (true ? -1.0 : 1.0))), foo(vec3(0.5, 0.5, (-(2.0 / -1.0) + ((0.0 * 0.5) + (false ? -1.0 : -1.0)))), vec2(-1.0, -1.0), 0.0), foo(vec3(((true ? (0.5 / 2.0) : (-1.0 / 0.5)) - 0.0), -+0.5, ((!false ? -2.0 : (2.0 / 2.0)) / 0.5)), vec2(0.0, ((1.0 + -1.0) / 2.0)), (+-1.0 / -1.0))), b = bar(), c = bar();
}

