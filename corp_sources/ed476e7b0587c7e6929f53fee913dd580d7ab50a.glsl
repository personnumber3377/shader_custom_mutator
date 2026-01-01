#version 300 es
uniform b {
  float f;
} blockInstance;void main() {
   gl_Position = vec4(blockInstance.f, 0.0, 0.0, 1.0);
}
