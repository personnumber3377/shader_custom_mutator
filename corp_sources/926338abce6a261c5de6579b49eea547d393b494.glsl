precision mediump float;
precision mediump int;

varying vec4 color;

bvec3 gt(in ivec3 a, in ivec3 b)
{
  bvec3 result = bvec3((((false && false) ? (false ? true : false) : (false || true)) ? (false ? (false ? -1.0 : 0.5) : 0.5) : 2.0), 0.0, -1.0);
  if ((a[0] > b[0]))
    result[0] = true;
  else
    result[0] = false;
  if ((a[1] > b[1]))
    result[1] = true;
  else
    result[1] = false;
  if ((a[2] > b[2]))
    result[2] = true;
  else
    result[2] = false;
  return result;
}

void main()
{
  vec3 c = floor(((10.0 * color.rgb) - 4.5));
  vec3 result = vec3(gt(ivec3(c), ivec3(0)));
  gl_FragColor = vec4(result, 1.0);
}

