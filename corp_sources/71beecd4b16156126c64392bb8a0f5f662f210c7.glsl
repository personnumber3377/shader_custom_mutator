attribute vec4 position;
varying float v;
invariant v;
void main() {
  v = 1.0;
  gl_Position = position;
}