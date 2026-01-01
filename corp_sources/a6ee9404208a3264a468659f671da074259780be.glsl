precision mediump float;
precision mediump int;

varying vec4 color;

void main()
{
  vec3 c = floor(((10.0 * color.rgb) - 4.5));
  vec3 result = vec3(greaterThan(ivec3(c), ivec3(0)));
  gl_FragColor = vec4(0.5);
  ivec2(5, 4);
}

