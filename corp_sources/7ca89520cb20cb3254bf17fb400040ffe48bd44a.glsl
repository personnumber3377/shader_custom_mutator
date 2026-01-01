#pragma STDGL invariant(all)
varying vec4 v_varying;
void main() {
  gl_Position = v_varying;
}