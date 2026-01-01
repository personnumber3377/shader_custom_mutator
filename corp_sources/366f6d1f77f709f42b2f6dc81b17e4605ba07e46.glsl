#version 300 es
in vec4 __position;
out float v;
void main() {
  v = 1.0;
  gl_Position = __position;
}