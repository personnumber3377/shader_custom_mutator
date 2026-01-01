precision mediump float;
precision mediump int;

varying vec4 color;

bvec2 eq(in bvec2 a, in bvec2 b)
{
  bvec2 result;
  if ((a[0] == b[0]))
    result[0] = true;
  else
    result[0] = false;
  if ((a[1] == b[1]))
    result[1] = true;
  else
    result[1] = false;
  return result;
}

void main()
{
  vec2 c = floor((1.5 * color.rg));
  vec2 result = vec2(eq(bvec2(c), bvec2(true)));
  gl_FragColor = vec4(result, 0.0, 1.0);
}

