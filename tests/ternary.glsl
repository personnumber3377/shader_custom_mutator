precision mediump float;
precision mediump int;

void main() {
    float a = 0.0, b = 0.0, c = 0.0, d = 0.0;
    float w = (a ? a,b : b,c);
    float z = a ? b ? c : d : w;
}
