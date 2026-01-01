precision mediump float;
precision mediump int;

precision mediump float;
void main()
{
    vec2 v = vec2(1,5);
    v.xy += v.yx += v.xy;
    vec2 v1 = v, v2 = v;
    v1.xy += v2.yx += ++(v.xy);
    v1.xy += v2.yx += (v.xy)++;
    gl_FragColor = vec4(v1,v2);
}
