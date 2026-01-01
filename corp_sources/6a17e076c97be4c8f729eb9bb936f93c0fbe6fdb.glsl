precision mediump float;
precision mediump int;

precision mediump float;
void main()
{
    vec4 v = vec4(5,6,7,8);
    v.wzyx.zywx.wzy.zy = (v.wzyx.zywx.wx)++;
    gl_FragColor = vec4(v);
}
