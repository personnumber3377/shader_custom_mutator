#version 300 es
struct st { mat2 m; };layout(row_major) uniform b {
  st s;
};void main() {
   gl_Position = vec4(s.m);
}
