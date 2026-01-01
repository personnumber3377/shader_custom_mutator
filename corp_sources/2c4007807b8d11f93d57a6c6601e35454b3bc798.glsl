#version 300 es
struct st { float f; };uniform b {
  st s;
} instanceName;void main() {
   gl_Position = vec4(instanceName.s.f, 0.0, 0.0, 1.0);
}
