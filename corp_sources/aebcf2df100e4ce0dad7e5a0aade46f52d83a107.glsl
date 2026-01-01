precision mediump float;
precision mediump int;

precision mediump float;
uniform float viewportwidth;
uniform float viewportheight;
void main()
{
	gl_FragColor = vec4(gl_FragCoord.x /viewportwidth , gl_FragCoord.y/viewportheight, 0.0, 1.0);
}
