#version 300 es
in vec4 position__;
out float v;
void main() {
  v = 1.0;
  gl_Position = position__;
}