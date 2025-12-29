uniform sampler2D samp2D;
vec4 v1 = vec4(2.0, 3.0, 5.0, 7.0);
vec4 v2 = vec4(11.0, 13.0, 17.0, 19.0);
vec4 v3 = vec4(23.0, 29.0, 31.0, 37.0);
vec4 v4 = vec4(41.0, 43.0, 47.0, 53.0);
struct str {
    int a;
    vec2 b[3];
    bool c;
};
void main()
{
    mat4 m = mat4(v1, v2, v3, v4);
    mat4 mm  = matrixCompMult(m, m);
    float f = mm[1].w;
    float g = matrixCompMult(m, m)[2].y;
    float h = str(1, vec2[3](vec2(2.0, 3.0), vec2(4.0, 5.0), vec2(6.0, 7.0)), true).b[1][1];
    float i = texture(samp2D, vec2(0.5,0.5)).y;
    i += (i > 0.1 ? v1 : v2)[3];
    str t;
    i += (t = str(1, vec2[3](vec2(2.0, 3.0), vec2(4.0, 5.0), vec2(6.0, 7.0)), true)).b[2].y;
    gl_FragColor = vec4(f, g, h, i);
}
