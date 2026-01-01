attribute vec4 position;
void main() {
   gl_Position = position + vec4(gl_DepthRange.near, gl_DepthRange.far, gl_DepthRange.diff, 1.0);
}
