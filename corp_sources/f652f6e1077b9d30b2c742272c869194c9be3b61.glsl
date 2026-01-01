precision mediump float;
precision mediump int;

vec4 webgl_foo() {
  return vec4(1.0);
}
void main() {
  gl_Position = webgl_foo();
}
