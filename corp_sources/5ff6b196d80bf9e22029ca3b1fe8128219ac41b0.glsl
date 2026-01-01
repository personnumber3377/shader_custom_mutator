precision mediump float;
precision mediump int;

precision mediump float;
struct s{
    float f;
    vec3  v;
} s1 ;
void main()
{
    vec4 v = vec4(float(vec2(1,2)), 5,6,7);
    vec4 v1 = vec4(3, vec2(ivec2(1,2)), 4);
    vec4 v2 = vec4(8, 9, vec4(ivec4(1,2,3,4)));
    vec2 v3 = vec2(v2);
    vec4 v4 = vec4(v3, v2.z, v2.w);
    const vec4 v5 = vec4(2.0, s(2.0, vec3(3,4,5)).v);
    gl_FragColor = v5 + v + v1 + v4 ;
}
