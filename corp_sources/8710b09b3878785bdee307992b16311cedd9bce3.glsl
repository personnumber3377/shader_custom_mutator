#version 300 es
uniform blockName {
  float field;
} blockInstance;void main() {
   gl_Position = vec4(blockInstance.field, 0.0, 0.0, 1.0);
}
