uniform sampler2D s[];
uniform U0 {
    vec4 a[2];
} u0;
uniform U1 {
    vec4 a[];
} u1;
buffer B0 {
    vec4 a[5];
} b0;
buffer B1 {
    vec4 a[];
} b1;
buffer B2 {
    vec4 a[];
} b2[2];
in vec4 out_VS;
out vec4 o;
void main() {
    o = texture(s[6], out_VS.xy);
    o = u1.a[12];
    o = b1.a[4];
}
