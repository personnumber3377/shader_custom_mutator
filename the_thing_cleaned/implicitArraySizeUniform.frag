uniform float f0[];
uniform sampler2D s0[];
uniform sampler2D s1[];
uniform U0 {
    vec4 a[];
} u0;
uniform U1 {
    vec4 a[];
} u1;
buffer B0 {
    vec4 a;
} b0[];
buffer B1 {
    vec4 a[11];
} b1;
buffer B2 {
    vec4 a[];
} b2;
in vec4 out_VS;
out vec4 o;
void main() {
    o = texture(s0[nonuniformEXT(1)], gl_FragCoord.xy);
    o += u1.a[6];
    o += b0[9].a;
    o += b2.a[nonuniformEXT(1)];
}
