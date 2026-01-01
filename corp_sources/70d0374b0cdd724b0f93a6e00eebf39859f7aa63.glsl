#version 300 es
uniform b {
  float f;
};void main() {
   gl_Position = vec4(f, 0.0, 0.0, 1.0);
}
